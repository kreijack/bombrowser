"""
BOM Browser - tool to browse a bom
Copyright (C) 2022 Goffredo Baroncelli <kreijack@inwind.it>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import socketserver
import socket
import pickle
import struct
import sys
import time

import db

class RemoteSQLClient:
    def __init__(self, addr='127.0.0.1', port=8765):
        self._port = port
        self._addr = addr
        self._username = None
        self._password = None
        self._format = "!bbhl"
        self._sock = None

    def _remote_call(self, func_name, *args, **kwargs):
        if self._sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._addr, self._port))

            if self._username and self._password:
                self.remote_server_do_auth(self._username, self._password)

        data = pickle.dumps((func_name, args, kwargs))
        header = struct.pack(self._format, 0, # rev
            0, # unused
            0, # unused
            len(data))

        try:
            self._sock.sendall(header)
        except:
            self._sock.close()
            self._sock = None
            raise
        self._sock.sendall(data)

        header = bytes([])
        while len(header) != struct.calcsize(self._format):
            d = self._sock.recv(struct.calcsize(self._format) - len(header))
            if len(d) == 0:
                time.sleep(0.1)
                continue
            header += d
        ver, _, _, datasize = struct.unpack(self._format, header)
        assert(ver == 0)

        data = bytes([])
        while datasize > 0:
            d = self._sock.recv(4096)
            if len(d) == 0:
                time.sleep(0.1)
                continue
            datasize -= len(d)
            data += d

        ret, excp = pickle.loads(data)
        if excp:
            raise Exception(excp)
        if func_name == "remote_server_do_auth" and ret:
            self._username = args[0]
            self._password = args[1]

        return ret

    def __getattr__(self, name):
        class Caller:
            def __init__(self, name, conn):
                self._name = name
                self._conn = conn
            def __call__(self, *args, **kwargs):
                return self._conn._remote_call(self._name, *args, **kwargs)
        return Caller(name, self)


class _ServerHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):

        remote_db_instance = \
            RemoteSQLServer(self.server._server_data["db_instance"])
        self.server._server_data["clients_count"] += 1
        self.server._server_data["client_seq"] += 1
        if self.server._server_data["verbose"]:
            print("Got connection:",
                "id=", self.server._server_data["client_seq"],
                "count=", self.server._server_data["clients_count"]
            )
        format_ = "!bbhl"
        while True:
            header = self.request.recv(struct.calcsize(format_))
            if len(header) == 0:
                break
            ver, _, _, datasize = struct.unpack(format_, header)
            assert(ver == 0)
            data = bytes([])
            while datasize > 0:
                d = self.request.recv(4096)
                datasize -= len(d)
                data += d        
            
            name, args, kwargs = pickle.loads(data)
            if name == "remote_server_get_info":
                excp = None
                ret = {
                    "clients_count": self.server._server_data["clients_count"],
                    "id": self.server._server_data["client_seq"],
                }
            elif name == "remote_server_get_id":
                excp = None
                ret = self.server._server_data["client_seq"]
            elif hasattr(remote_db_instance, name):
                try:
                    ret = getattr(remote_db_instance, name)(*args, **kwargs)
                    excp = None
                except Exception as e:
                    excp = e
                    ret = None

            data = pickle.dumps((ret, excp))
            header = struct.pack(format_, 0, # rev
                0, # unused
                0, # unused
                len(data))
            self.request.sendall(header)
            self.request.sendall(data)

        self.server._server_data["clients_count"] -= 1
        if self.server._server_data["verbose"]:
            print("End connection:",
                "id=", self.server._server_data["client_seq"],
                "count=", self.server._server_data["clients_count"]
            )


class RemoteSQLServer:
    """This is an 'instance for connection' class"""
    def __init__(self, db):
        self._read_only_methods = [
            "search_revisions",
            "get_config",
            "get_children_by_rid",
            "get_bom_dates_by_code_id",
            "get_drawings_by_code_id",
            "get_where_used_from_id_code",
            "get_bom_by_code_id3",
            "is_child",
            "is_assembly",
            "get_children_dates_range_by_rid",
            "get_parent_dates_range_by_code_id",
            "get_dates_by_code_id3",
            "get_codes_by_like_code_and_descr",
            "get_codes_by_like_descr",
            "get_codes_by_like_code",
            "get_codes_by_code",
            "get_code_by_rid",
            "get_code",
            "dump_tables",
            "list_main_tables",
            "dump_table",
        ]
        self._read_write_methods = [
            "delete_code_revision",
            "delete_code",
            "update_dates",
            "update_by_rid2",
            "revise_code",
            "copy_code",
            "create_db",
        ]
        self._db = db
        self._allow_access = False
        self._read_only = True

    def remote_server_do_auth(self, name, password):
        self._allow_access = True
        self._read_only = False       
        return True

    def __getattr__(self, name):
        if not self._allow_access:
            raise Exception("You have to authenticate")

        if (name in self._read_write_methods and self._read_only):
            raise Exception("Access read only")
            
        if (not name in self._read_write_methods and
            not name in self._read_only_methods):
                raise Exception("Unknown method '%s'"%(name))

        if not callable(getattr(self._db, name)):
                raise Exception("Method '%s' is not callable"%(name))

        return getattr(self._db, name)


def _start_server(db_instance, addr='0.0.0.0', port=8765, verbose=False):
    class Server_(socketserver.ThreadingTCPServer):
        allow_reuse_address = True

        def __init__(self, *args):
            super().__init__(*args)
            self._server_data = {
                "verbose": verbose,
                "clients_count": 0,
                "db_instance": db_instance,
                "client_seq": 1000,
            }

            if (verbose):
                print("Start server: %s@%d"%(args[0]))

    with Server_((addr, port), _ServerHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

def main():
    if sys.argv[1] == "--client-test":
        r = RemoteSQLClient()
        r.remote_server_do_auth("foo", "bar")
        print("r.remote_server_get_id:", r.remote_server_get_id())
        print("list_main_tables: ", r.list_main_tables())
        print("r.remote_server_get_id:", r.remote_server_get_id())
        #print("get_codes_by_like_code:", r.get_codes_by_like_code("%"))
        print("r.remote_server_get_id:", r.remote_server_get_id())

        r2 = RemoteSQLClient()
        r2.remote_server_do_auth("foo", "bar")
        print("r.remote_server_get_id:", r2.remote_server_get_id())
        print("list_main_tables: ", r2.list_main_tables())
        print("r.remote_server_get_id:", r2.remote_server_get_id())
        #print("get_codes_by_like_code:", r2.get_codes_by_like_code("%"))
        print("r.remote_server_get_id:", r2.remote_server_get_id())

    elif sys.argv[1] == "--server":
        import cfg
        cfg.init()

        dbtype = cfg.config().get("LOCALBBSERVER", "db")
        host = cfg.config().get("LOCALBBSERVER", "host")
        port = int(cfg.config().get("LOCALBBSERVER", "port"))
        verbose = int(cfg.config().get("LOCALBBSERVER", "verbose"))
        connection,instance = db._create_db(dbtype)
        _start_server(instance, host, port, verbose)

if __name__ == "__main__":
    main()
