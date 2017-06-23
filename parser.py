import sys
from algo import Delta, optimize

stock = dict()
productName = ""
process = dict()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("One arg please")
        exit(0)
    try: 
        f = open(sys.argv[1], "r")
        full = f.read()
        arr = full.split('\n')
        for elem in arr:
            if len(elem) >= 1 and elem[0] == '#':
                continue
            elif elem.find("optimize") != -1  and elem.index("optimize") == 0:
                productName = elem[elem.index(":")+2:len(elem)-1]
            elif elem.count(':') == 1:
                stock[elem[:elem.index(":")]] = int(elem[elem.index(":")+1:])
            elif len(elem) > 1:
                processName = elem[:elem.index(":")]
                process[processName] = {"ingredients": {}, "products": {}, "time": 0}
                elem = elem[elem.index(":")+1:]
                ingredientsTab = elem[1:elem.index(")")].split(';')
                for val in ingredientsTab:
                    process[processName]["ingredients"][val[:val.index(":")]] = int(val[val.index(":")+1:])
                elem = elem[1:]
                productsTab = elem[elem.index("(")+1:]
                productsTab = productsTab[:productsTab.index(")")].split(";")
                for val in productsTab:
                    process[processName]["products"][val[:val.index(":")]] = int(val[val.index(":")+1:])
                elem = elem[elem.rfind(":")+1:]
                process[processName]['time'] = int(elem)
    except Exception as e:
        print("Parsing error: ",e)

    delta = Delta(stock)
    delta = optimize(process, productName, delta, 10)

    print("delta processes: " + delta.processChain + "\nstock: " + delta.stock)
