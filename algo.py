import copy

class Delta():
    def __init__(self, stock):
        self.stock = stock
        self.processChain = []
        self.time = 0

def makeRecepies(stock, ingredients, products):
    newStock = stock.copy()
    for key, value in ingredients.items():
        newStock[key] -= value
        if newStock[key] < 0:
            return newStock, False
    for key, value in products.items():
        newStock[key] += value
    return newStock, True

def optimize(processes, productName, delta, depth):
    if depth == 0:
        return delta
    bestDelta = copy.deepcopy(delta)
    for pName, p in processes.items():
        pStock, pSuccess = makeRecepies(delta.stock, p['ingredients'], p['products'])
        if pSuccess:
            pDelta = Delta(pStock)
            pDelta.processChain += pName
            pDelta.time += p['time']
            newDelta = optimize(
                processes,
                productName,
                pDelta,
                depth-1
            )
            if (newDelta.stock[productName] > bestDelta.stock[productName] or
                (newDelta.stock[productName] == bestDelta.stock[productName] and
                 newDelta.time < bestDelta.time)):
                bestDelta = newDelta
    return bestDelta
