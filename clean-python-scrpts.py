import os

files = [x for x in os.listdir(".") if x.upper().endswith(".PY")]
for filename in files:
    prg = open(filename).readlines()
    
    objs = []
    for line in prg:
        i = line.find("import ")
        if i < 0:
            continue
            
        objs.extend(map(lambda x: x.strip(), line[i+7:].split(",")))

    toremove = set()
    for obj in objs:
        found = False
        for line in prg:
            i = line.find("import ")
            if i >= 0:
                continue
                
            if obj in line:
                found = True
                break
                
        if not found:
            toremove.add(obj)

    if len(toremove) == 0:
        continue
        
    print(filename)
    for obj in toremove:
        print("\t", obj)
    print()
    print("-"*60)
    
    for line in prg:
        i = line.find("import ")
        if i < 0:
            continue

        obj = set(map(lambda x: x.strip(), line[i+7:].split(",")))
        print(line[:i+7], ", ".join(list(obj.difference(toremove))))
    
    print("-"*60)
    print()
        
