from ast import Str
import math
from random import random
import random

class CacheConfig():
    def __init__(self, nsets, blockSize, associativity, byteAddress):
        self.cacheSize = (nsets * blockSize * associativity)/8 # Convert the first argument into KB, 32 = 32KB, 64 = 64KB, 128 = 128KB, 256 = 256KB
        self.byteAddress = byteAddress # 8 bits = 1 byte
        self.blockSize =  blockSize # 8 bits = 1 byte
        self.memoryAddressSize = 32 # 32 or 64 bits
        self.associativeWays = associativity # 1 = Direct Mapping, 2 = 2-way associative, 4 = 4-way associative, 8 = 8-way associative, 16 = 16-way associative
        
        self.cacheLines = nsets  #Cache index size
        self.index = int(math.log(self.cacheLines,2)) # number of bits for index
        self.des = int(math.log(self.blockSize/self.byteAddress,2)) # number of bits for des
        self.trueCacheSize = round(((self.cacheLines * self.associativeWays) * (self.blockSize + (self.memoryAddressSize - self.index - self.des)+1))/8192, 2) # Conversion for true cache size in KB 
        print("\n[Cache Configuration]")
        print(f'Index: {self.index}b\t Tag:{self.memoryAddressSize-self.index-self.des}b\t Des:{self.des}b\t CacheLines:{self.cacheLines}\t AssociativeWays:{self.associativeWays}')
        print(f'BlockSize:{int(self.blockSize/8)}B\t ByteAddress: {int(self.byteAddress/8)}B\t MemoryAddressSize: {self.memoryAddressSize}b\t ')
        print(f'CacheSize:{int(self.cacheSize/1024)}KB\t TrueCacheSize: {self.trueCacheSize}KB\t TrueCacheSize is {100 * float(self.trueCacheSize)/(self.cacheSize/1024)- 100}% bigger')

def startCache(cl):
    cacheMemory = {}
    for i in range(cl):
        cacheMemory[i] = {'tag':0,'val':0,'data':0}
    return cacheMemory

def checkCache(cacheMemory):
    for acessNumber in cacheMemory:
        if cacheMemory[acessNumber]['val'] == 0:
            return False
    return True

def cacheDirectMapAccess(DirectMap, memoryAcess, outputFlag):

    cl = DirectMap.cacheLines
    cm = startCache(cl)
    des = DirectMap.des
    index = DirectMap.index

    hit = 0
    miss = 0
    compulsoryMiss = 0
    capacityMiss = 0
    conflictMiss = 0
    
    for binary in memoryAcess:
        if des == 0:
            cmIndex = int(binary[32-index:],2)
        else:
            cmIndex = int(binary[32-des-index:-des],2)

        if  cm[cmIndex]['val'] == 1:
            if  cm[cmIndex]['tag'] == binary[:-des-index]:
                hit = hit + 1
            else:
                miss = miss +1
                conflictMiss = conflictMiss + 1
                cm[cmIndex]['tag'] = binary[:-des-index]
                cm[cmIndex]['val'] = 1
                if checkCache(cm) == False:
                    capacityMiss = capacityMiss + 1
        else:
            miss = miss + 1
            compulsoryMiss = compulsoryMiss + 1
            cm[cmIndex]['tag'] = binary[:-des-index]
            cm[cmIndex]['val'] = 1
    print("\n[Cache Simulation]")   
    if int(outputFlag) == 0:
        print(f'Hit:{hit}\t Miss:{miss}\t HitRate:{round(hit/len(memoryAcess)*100, 3)}%\t TotalAccess:{hit+miss}')
        print(f'MissCompulsory:{compulsoryMiss}\t MissConflict:{conflictMiss}\t MissCapacity:{capacityMiss}\t')
    else:
        print(f'{hit+miss}, {round(hit/len(memoryAcess)*100, 3)}, {round(miss/len(memoryAcess)*100, 3)}, {round(compulsoryMiss/len(memoryAcess)*100, 3)}, {round(capacityMiss/len(memoryAcess)*100, 3)}, {round(conflictMiss/len(memoryAcess)*100, 3)}')
        return f'{hit+miss}, {round(hit/len(memoryAcess)*100, 3)}, {round(miss/len(memoryAcess)*100, 3)}, {round(compulsoryMiss/len(memoryAcess)*100, 3)}, {round(capacityMiss/len(memoryAcess)*100, 3)}, {round(conflictMiss/len(memoryAcess)*100, 3)}'

def cacheAssociativeMapAccess(DirectMap, memoryAcess, outputFlag):
    cl = DirectMap.cacheLines
    des = DirectMap.des
    index = DirectMap.index

    hit = 0
    miss = 0

    compulsoryMiss = 0
    capacityMiss = 0
    conflictMiss = 0

    cm = [startCache(cl) for i in range(DirectMap.associativeWays)]
    
    for binary in memoryAcess:
        if des == 0:
            cmIndex = int(binary[32-index:],2)
        else:
            cmIndex = int(binary[32-des-index:-des],2)

        isTagTrue = False
        for j in range(DirectMap.associativeWays):
            if  cm[j][cmIndex]['val'] == 1:
                if  cm[j][cmIndex]['tag'] == binary[:-des-index]:
                    hit = hit + 1
                    isTagTrue = True
                    break

        if isTagTrue == False:
            miss = miss + 1
            compulsoryMiss = compulsoryMiss + 1
            isPositionFree = False
            for j in range(DirectMap.associativeWays):
                if  cm[j][cmIndex]['val'] == 0:
                    cm[j][cmIndex]['tag'] = binary[:-des-index]
                    cm[j][cmIndex]['val'] = 1
                    cm[j][cmIndex]['data'] = binary
                    isPositionFree = True
                    break
            
            if isPositionFree == False:
                conflictMiss = conflictMiss + 1
                addRandom = int(random.randrange(0, DirectMap.associativeWays))
                if checkCache(cm[addRandom]) == False:
                    capacityMiss = capacityMiss + 1
                cm[addRandom][cmIndex]['tag'] = binary[:-des-index]
                cm[addRandom][cmIndex]['val'] = 1
                cm[addRandom][cmIndex]['data'] = binary

    print("\n[Cache Simulation]")        
    if int(outputFlag) == 0:
        print(f'Hit:{hit}\t Miss:{miss}\t HitRate:{round(hit/len(memoryAcess)*100, 3)}%\t TotalAccess:{hit+miss}')
        print(f'MissCompulsory:{compulsoryMiss}\t MissConflict:{conflictMiss}\t MissCapacity:{capacityMiss}\t')
    else:
        print(f'{hit+miss}, {round(hit/len(memoryAcess)*100, 3)}, {round(miss/len(memoryAcess)*100, 3)}, {round(compulsoryMiss/len(memoryAcess)*100, 3)}, {round(capacityMiss/len(memoryAcess)*100, 3)}, {round(conflictMiss/len(memoryAcess)*100, 3)}')
        return f'{hit+miss}, {round(hit/len(memoryAcess)*100, 3)}, {round(miss/len(memoryAcess)*100, 3)}, {round(compulsoryMiss/len(memoryAcess)*100, 3)}, {round(capacityMiss/len(memoryAcess)*100, 3)}, {round(conflictMiss/len(memoryAcess)*100, 3)}'
