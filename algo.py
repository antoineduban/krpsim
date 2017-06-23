import copy

class Delta():
    def __init__(self, stock):
        self.stock = stock
        self.processChain = []
        self.time = 0
    def __str__(self):
        return ("stock: " + str(self.stock) + "\n" +
                "processChain: " + str(self.processChain) + "\n" +
                "time: " + str(self.time) + "\n")

def makeRecepies(stock, ingredients, products):
    newStock = stock.copy()
    for key, value in ingredients.items():
        if key not in newStock:
            return newStock, False
        newStock[key] -= value
        if newStock[key] < 0:
            return newStock, False
    for key, value in products.items():
        if key not in newStock:
            newStock[key] = value
        else:
            newStock[key] += value
    return newStock, True

def optimize(processes, productName, delta, depth):
    if depth == 0:
        return delta
    bestDelta = copy.deepcopy(delta)
    for pName, p in processes.items():
        pDelta = copy.deepcopy(delta)
        pDelta.stock, pSuccess = makeRecepies(delta.stock, p['ingredients'], p['products'])
        pDelta.processChain.append(pName)
        pDelta.time += p['time']
        if pSuccess:
            pDelta = optimize(
                processes,
                productName,
                pDelta,
                depth-1
            )
        if (productName in pDelta.stock and
            (productName not in bestDelta.stock or
             pDelta.stock[productName] > bestDelta.stock[productName] or
             (pDelta.stock[productName] == bestDelta.stock[productName] and
              pDelta.time < bestDelta.time))):
            bestDelta = pDelta
    return bestDelta

