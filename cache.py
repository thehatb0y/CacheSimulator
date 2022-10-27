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
        
        print(f'\nIndex: {self.index}b\t Tag:{self.memoryAddressSize-self.index-self.des}b\t Des:{self.des}b\t CacheLines:{self.cacheLines}\t AssociativeWays:{self.associativeWays}')
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

def cacheDirectMapAccess(DirectMap, memoryAcess):
    cl = DirectMap.cacheLines
    cm = startCache(cl)
    des = DirectMap.des
    index = DirectMap.index

    hit = 0
    miss = 0
    compulsoryMiss = 0
    capacityMiss = 0
    conflictMiss = 0

    for acessNumber in memoryAcess:
        address = int(acessNumber)
        #convert address to binary
        binary = bin(int(address))
        if  cm[address%cl]['val'] == 1:
            if  cm[address%cl]['tag'] == binary[:-des-index]:
                hit = hit + 1
            else:
                miss = miss +1
                conflictMiss = conflictMiss + 1
                cm[address%cl]['tag'] = binary[:-des-index]
                cm[address%cl]['val'] = 1
                cm[address%cl]['data'] = binary
        else:
            miss = miss + 1
            compulsoryMiss = compulsoryMiss + 1
            cm[address%cl]['tag'] = binary[:-des-index]
            cm[address%cl]['val'] = 1
            cm[address%cl]['data'] = binary

    #Total de acessos, Taxa de hit, Taxa de miss, Taxa de miss compulsório, Taxa de miss de capacidade, Taxa de miss de conflito 
    print(f'Hit:{hit}\t Miss:{miss}\t HitRate:{round(hit/len(memoryAcess)*100, 3)}%\t TotalAccess:{hit+miss}')
    print(f'MissCompulsory:{compulsoryMiss}\t MissConflict:{conflictMiss}\t')
    return round(hit/len(memoryAcess)*100, 3)

def cacheAssociativeMapAccess(DirectMap, memoryAcess):
    cl = DirectMap.cacheLines
    des = DirectMap.des
    index = DirectMap.index

    hit = 0
    miss = 0
    missCompulsory = 0
    missConflict = 0
    missCapacity = 0

    #create a list of cacheMemory, the list have size of associativeWays and each item from the list should call startCache function
    cm = [startCache(cl) for i in range(DirectMap.associativeWays)]

    #check check if tag = 0 in each cm list
    for acessNumber in memoryAcess:
        #set address as a random from 0 to ramSize
        address = int(acessNumber)
        #convert address to binary
        binary = bin(address)
        count = 0
        isTagTrue = False
        for j in range(DirectMap.associativeWays):
            if  cm[j][address%cl]['val'] == 1:
                if  cm[j][address%cl]['tag'] == binary[:-des-index]:
                    hit = hit + 1
                    isTagTrue = True
                    break

        if isTagTrue == False:
            miss = miss + 1
            isPositionFree = False
            for j in range(DirectMap.associativeWays):
                if  cm[j][address%cl]['val'] == 0:
                    cm[j][address%cl]['tag'] = binary[:-des-index]
                    cm[j][address%cl]['val'] = 1
                    cm[j][address%cl]['data'] = binary
                    isPositionFree = True
                    break
            
            if isPositionFree == False:
                missConflict = missConflict + 1
                addRandom = int(random.randrange(0, DirectMap.associativeWays))
                cm[addRandom][address%cl]['tag'] = binary[:-des-index]
                cm[addRandom][address%cl]['val'] = 1
                cm[addRandom][address%cl]['data'] = binary
            
    print(f'Hit:{hit}\t Miss:{miss}\t HitRate:{round(hit/len(memoryAcess)*100, 3)}%\t TotalAccess:{hit+miss}')
    return round(hit/len(memoryAcess)*100, 3)
