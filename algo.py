import copy
from heapq import nlargest
import random


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


def getRandomChain(processes, delta):
    pDelta = copy.deepcopy(delta)
    count = 0
    for i in range(100):
        it = random.choice(list(processes.keys()))
        pDelta.stock, pSuccess = makeRecepies(delta.stock, processes[it]['ingredients'], processes[it]['products'])
        pDelta.processChain.append(it)
        pDelta.time += processes[it]['time']
        if pSuccess == True:
            count += 1
            if count == 10:
                break
    return pDelta


def getRandomSet(processes, delta, productName):
    chains = []
    for i in range(100):
        chains.append(getRandomChain(processes, delta))
    for val in chains:
        if not productName in val.stock:
            val.stock[productName] = 0
    return chains


def cross(x, y):
    new1 = []
    new2 = []
    it = random.randint(0, len(x.processChain)-1)
    c = 0
    for i in x.processChain:
        if (c < it):
            new1.append(i)
        else:
            new1.append(y.processChain[c])
        c += 1
    c = 0
    for i in y.processChain:
        if (c < it):
            new2.append(i)
        else:
            new2.append(x.processChain[c])
        c += 1
    x.processChain = new1
    y.processChain = new2
    return x, y

def mutate(s):
    it = random.randint(0, len(s.processChain)-1)
    it2 = random.randint(0, len(s.processChain)-1)
    tmp = s.processChain[it]
    s.processChain[it] = s.processChain[it2]
    s.processChain[it2] = tmp
    return s

def applyToStock(s, processes):
    for val in s.processChain:
        for v in processes:
            if val == v:
                tmpStock, pSuccess = makeRecepies(s.stock, processes[v]['ingredients'], processes[v]['products'])
                if (pSuccess == True):
                    s.stock = tmpStock.copy()
                else:
                    return s
    return s

def crossAndMutate(bests, processes):
    newSet = []
    for x in bests:
        for y in bests:
            new1, new2 = cross(x, y)
            new1 = mutate(new1)
            new2 = mutate(new2)
            new1 = applyToStock(new1, processes)
            new2 = applyToStock(new2, processes)
            newSet.append(new1)
            newSet.append(new2)
    return newSet


def resetStocks(bests, initStock):
    for val in bests:
        val.stock = initStock.copy()
    return bests

def evolve(chains, depth, productName, processes, initStock):
    bests = nlargest(10, chains, key=lambda e:e.stock[productName])
    bests = resetStocks(bests, initStock)
    if (depth == 0):
        return bests
    newSet = crossAndMutate(bests, processes)
    return evolve(newSet, depth - 1, productName, processes, initStock) 

def genetic(processes, productName, delta, initStock):
    chains = getRandomSet(processes, delta, productName)
    bests = evolve(chains, 900, productName, processes, initStock)
    for val in bests:
        print(val)
