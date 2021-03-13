# Database Structure

## Database 0.1..0.2 (old)

The database structure consists by 3 main tables:
- items
- assemblies
- drawings

The *items* table stores the information related to the code. It contains the following fields:
- id
- code
- description
- version
[...]

The *assemblies* table, stores the link between the children and the parent. It contains the following fields:
- id
- parent_id
- child_id
- quantity
[...]

The *drawings* table, stores the documents path associated to an *items*. It contains the following fields:
- id
- item_id
- name
- path
[..]

Obviously *item_id*, *parent_id* and *child_id* are *foreign key*  of *items(id)* .

The table *database_props* contains a key/value pairs and it contains teh database settings.
The table *item_props* may contains further information for an item_revisions; currently it is not used.

## Database 0.3..04 (current)

The database structure consists by 4 main tables:
- items
- item_revisions
- assemblies
- drawings


The *items* table stores the information related to the code name *only*. It contains the following fields:
- id
- code

The *item_revision* table stores the information related to the revision of a code. It contains the following fields:
- id
- code_id
- description
- ver
[...]

The *assemblies* table, stores the link between the children and the parent. It contains the following fields:
- id
- revision_id
- child_id
- quantity
[...]

The *drawings* table, stores the documents path associated to an *items*. It contains the following fields:
- id
- revision_id
- name
- path
[..]

*assemblies.child_id*  and *item_revision.code_id* are *foreign key*  of *items(id)* .
*assemblies.revision_id*, *drawings.revision_id* are *foreign key*  of *item_revisions(id)* .

*item_revision.gvalXX* are 'free fields' to store arbitrary information.

The fields *item_revision.note* and *item_revision.type* are not used.
The fields *item_revision.gval9*..*item_revision.gval20* are not used.

The table *database_props* contains a key/value pairs and it contains teh database settings.
The table *item_props* may contains further information for an item_revisions; currently it is not used.


### Database v0.3

```SQL
            --
            -- ver 0.3
            --
            DROP INDEX IF EXISTS items.item_code_idx;
            DROP INDEX IF EXISTS items.item_code_ver_idx;
            DROP INDEX IF EXISTS items.item_code_ver_iter;
            DROP INDEX IF EXISTS drawings.drawing_idx;
            DROP INDEX IF EXISTS drawings.assemblies_child_idx;
            DROP INDEX IF EXISTS drawings.assemblies_parent_idx;

            DROP TABLE IF EXISTS assemblies;
            DROP TABLE IF EXISTS item_properties;
            DROP TABLE IF EXISTS database_props;
            DROP TABLE IF EXISTS drawings;
            DROP TABLE IF EXISTS item_revisions;
            DROP TABLE IF EXISTS items;

            CREATE TABLE    items (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code        VARCHAR(255) UNIQUE NOT NULL
            );

            CREATE INDEX item_code_idx             ON items(code);

            CREATE TABLE item_revisions (
                id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code_id         INTEGER,
                date_from       VARCHAR(10) NOT NULL DEFAULT '2000-01-01',
                date_to         VARCHAR(10) DEFAULT '',
                date_from_days  INTEGER DEFAULT 0,          -- 2000-01-01
                date_to_days    INTEGER DEFAULT 999999,
                ver             VARCHAR(10) NOT NULL,
                iter            INTEGER,
                type            VARCHAR(255),
                note            VARCHAR(255),
                descr           VARCHAR(255) NOT NULL,
                default_unit    VARCHAR(10) NOT NULL,
                gval1           VARCHAR(255) DEFAULT '',
                gval2           VARCHAR(255) DEFAULT '',
                gval3           VARCHAR(255) DEFAULT '',
                gval4           VARCHAR(255) DEFAULT '',
                gval5           VARCHAR(255) DEFAULT '',
                gval6           VARCHAR(255) DEFAULT '',
                gval7           VARCHAR(255) DEFAULT '',
                gval8           VARCHAR(255) DEFAULT '',

                FOREIGN KEY (code_id) REFERENCES items(id)
            );

            CREATE INDEX revision_code_id ON item_revisions(code_id);
            CREATE INDEX revision_code_id_date ON
                item_revisions(code_id, date_from_days);
            CREATE INDEX revision_date_from ON item_revisions(date_from);
            CREATE INDEX revision_date_from_days ON item_revisions(date_from_days);
            CREATE INDEX revision_date_to ON item_revisions(date_to);
            CREATE INDEX revision_date_to_days ON item_revisions(date_to_days);
            CREATE UNIQUE INDEX revision_code_iter
                ON item_revisions(code_id, iter);

            CREATE TABLE item_properties (
                id          INTEGER NOT NULL PRIMARY KEY,
                descr       VARCHAR(255),
                value       VARCHAR(1024),
                revision_id     INTEGER,

                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );
            CREATE UNIQUE INDEX item_prop_descr_rid ON item_properties(revision_id, descr);

            CREATE TABLE assemblies (
                id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                unit            VARCHAR(10),
                child_id        INTEGER,
                revision_id     INTEGER,
                qty             FLOAT,
                each            FLOAT DEFAULT 1.0,
                ref             VARCHAR(600) DEFAULT '',

                FOREIGN KEY (child_id) REFERENCES items(id),
                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );

            CREATE INDEX assemblies_child_idx ON assemblies(child_id);
            CREATE INDEX assemblies_revision_idx ON assemblies(revision_id);

            CREATE TABLE database_props (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                "key"       VARCHAR(255),
                value       VARCHAR(255)
            );

            INSERT INTO database_props ("key", value) VALUES ('ver', '0.4');

            CREATE TABLE drawings (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code        VARCHAR(255) DEFAULT '',
                revision_id INTEGER,
                filename    VARCHAR(255) NOT NULL,
                fullpath    VARCHAR(255) NOT NULL,

                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );
```


### Database v0.4

Differences between v0.4 and v0.3:
The following items are added:
- item_revisions.gval9 .. item_revisions.gval20
- item_revisions.type

The size of the following items are changed:
- assemblies.rev
- unit

```SQL
            --
            -- ver 0.4
            --
            DROP INDEX IF EXISTS items.item_code_idx;
            DROP INDEX IF EXISTS items.item_code_ver_idx;
            DROP INDEX IF EXISTS items.item_code_ver_iter;
            DROP INDEX IF EXISTS drawings.drawing_idx;
            DROP INDEX IF EXISTS drawings.assemblies_child_idx;
            DROP INDEX IF EXISTS drawings.assemblies_parent_idx;

            DROP TABLE IF EXISTS assemblies;
            DROP TABLE IF EXISTS item_properties;
            DROP TABLE IF EXISTS database_props;
            DROP TABLE IF EXISTS drawings;
            DROP TABLE IF EXISTS item_revisions;
            DROP TABLE IF EXISTS items;

            CREATE TABLE    items (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code        VARCHAR(255) UNIQUE NOT NULL
            );

            CREATE INDEX item_code_idx             ON items(code);

            CREATE TABLE item_revisions (
                id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code_id         INTEGER,
                date_from       VARCHAR(10) NOT NULL DEFAULT '2000-01-01',
                date_to         VARCHAR(10) DEFAULT '',
                date_from_days  INTEGER DEFAULT 0,          -- 2000-01-01
                date_to_days    INTEGER DEFAULT 999999,
                ver             VARCHAR(10) NOT NULL,
                iter            INTEGER,
                type            VARCHAR(255),
                note            VARCHAR(2048),
                descr           VARCHAR(255) NOT NULL,
                default_unit    VARCHAR(10) NOT NULL,
                gval1           VARCHAR(255) DEFAULT '',
                gval2           VARCHAR(255) DEFAULT '',
                gval3           VARCHAR(255) DEFAULT '',
                gval4           VARCHAR(255) DEFAULT '',
                gval5           VARCHAR(255) DEFAULT '',
                gval6           VARCHAR(255) DEFAULT '',
                gval7           VARCHAR(255) DEFAULT '',
                gval8           VARCHAR(255) DEFAULT '',
                gval9           VARCHAR(255) DEFAULT '',
                gval10          VARCHAR(255) DEFAULT '',
                gval11          VARCHAR(255) DEFAULT '',
                gval12          VARCHAR(255) DEFAULT '',
                gval13          VARCHAR(255) DEFAULT '',
                gval14          VARCHAR(255) DEFAULT '',
                gval15          VARCHAR(255) DEFAULT '',
                gval16          VARCHAR(255) DEFAULT '',
                gval17          VARCHAR(255) DEFAULT '',
                gval18          VARCHAR(255) DEFAULT '',
                gval19          VARCHAR(255) DEFAULT '',
                gval20          VARCHAR(255) DEFAULT '',

                FOREIGN KEY (code_id) REFERENCES items(id)
            );

            CREATE INDEX revision_code_id ON item_revisions(code_id);
            CREATE INDEX revision_code_id_date ON
                item_revisions(code_id, date_from_days);
            CREATE INDEX revision_date_from ON item_revisions(date_from);
            CREATE INDEX revision_date_from_days ON item_revisions(date_from_days);
            CREATE INDEX revision_date_to ON item_revisions(date_to);
            CREATE INDEX revision_date_to_days ON item_revisions(date_to_days);
            CREATE UNIQUE INDEX revision_code_iter
                ON item_revisions(code_id, iter);

            CREATE TABLE item_properties (
                id          INTEGER NOT NULL PRIMARY KEY,
                descr       VARCHAR(255),
                value       VARCHAR(1024),
                revision_id     INTEGER,

                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );
            CREATE UNIQUE INDEX item_prop_descr_rid ON item_properties(revision_id, descr);

            CREATE TABLE assemblies (
                id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                unit            VARCHAR(10),
                child_id        INTEGER,
                revision_id     INTEGER,
                qty             FLOAT,
                each            FLOAT DEFAULT 1.0,
                ref             VARCHAR(600) DEFAULT '',

                FOREIGN KEY (child_id) REFERENCES items(id),
                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );

            CREATE INDEX assemblies_child_idx ON assemblies(child_id);
            CREATE INDEX assemblies_revision_idx ON assemblies(revision_id);

            CREATE TABLE database_props (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                "key"       VARCHAR(255),
                value       VARCHAR(255)
            );

            INSERT INTO database_props ("key", value) VALUES ('ver', '0.4');

            CREATE TABLE drawings (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code        VARCHAR(255) DEFAULT '',
                revision_id INTEGER,
                filename    VARCHAR(255) NOT NULL,
                fullpath    VARCHAR(255) NOT NULL,

                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );
```
