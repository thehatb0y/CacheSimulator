import math
from random import random
import random
from PyQt5.QtGui import QColor
from fifo import fifo
from lru import lru

#CacheConfig build the cache
class CacheConfig():
    def __init__(self, nsets, blockSize, associativity, byteAddress):

        self.byteAddress = byteAddress # 8 bits = 1 byte
        self.blockSize =  blockSize*8 # 8 bits = 1 byte
        self.memoryAddressSize = 32 # 32 or 64 bits
        self.associativeWays = associativity # 1 = Direct Mapping, 2 = 2-way associative, 4 = 4-way associative, 8 = 8-way associative, 16 = 16-way associative
        self.cacheSize = (nsets * self.blockSize * associativity)/8 # Convert the first argument into KB, 32 = 32KB, 64 = 64KB, 128 = 128KB, 256 = 256KB
        self.cacheLines = nsets  #Cache index size
        self.index = int(math.log(self.cacheLines,2)) # number of bits for index
        self.des = int(math.log(self.blockSize/self.byteAddress,2)) # number of bits for des
        self.trueCacheSize = round(((self.cacheLines * self.associativeWays) * (self.blockSize + (self.memoryAddressSize - self.index - self.des)+1))/8192, 3) # Conversion for true cache size in KB 
        
        with open('CacheConfig.txt', 'w') as f: 
            f.write("\n[Cache Configuration]")
            f.write(f'\nIndex: {self.index}b\t Tag:{self.memoryAddressSize-self.index-self.des}b\t Des:{self.des}b\t CacheLines:{self.cacheLines}\t AssociativeWays:{self.associativeWays}')
            f.write(f'\nBlockSize:{int(self.blockSize/8)}B\t ByteAddress: {int(self.byteAddress/8)}B\t MemoryAddressSize: {self.memoryAddressSize}b\t ')
            f.write(f'\nCacheSize:{round(self.cacheSize/1024, 3)}KB\t TrueCacheSize: {self.trueCacheSize}KB\t \nTrueCacheSize is {round((100 * ((round((self.trueCacheSize), 3))/(round((self.cacheSize/1024),3)))- 100), 3)}% bigger')

#Start the cache with 0
def startCache(cl):
    cacheMemory = {}
    for i in range(cl):
        cacheMemory[i] = {'tag':0,'val':0,'data':0}
    return cacheMemory

#Check if the cache is full, return true
def checkCache(cacheMemory):
    for acessNumber in cacheMemory:
        if cacheMemory[acessNumber]['val'] == 0:
            return False
    return True

# Return: If outputflag = 0 return data + print , If outputflag = 1 return data
def cacheDirectMapAccess(DirectMap, memoryAcess, outputFlag, dataGrid):
    cl = DirectMap.cacheLines # cl = cache lines
    cm = startCache(cl) # cm = Cache memory, start the cache with 0
    des = DirectMap.des # des = displacement
    index = DirectMap.index # size of cache index in bits

    hit = 0
    miss = 0
    compulsoryMiss = 0
    capacityMiss = 0
    conflictMiss = 0
    
    #each 32 bits on the file is a memory acess in binary
    for binary in memoryAcess:
        #Gets the index of the binary
        if des == 0:
            cmIndex = int(binary[32-index:],2)
        else:
            if index == 0:
                cmIndex = 0
            else:
                cmIndex = int(binary[32-des-index:-des],2)

        #Using the Index that we got from the last step, we check if the tag is the same as the binary on the right position
        if  cm[cmIndex]['val'] == 1: #Before check the tag, we need to check the valid bit
            if  cm[cmIndex]['tag'] == binary[:-des-index]:
                hit = hit + 1 #If the tag is the same, we have a hit
            else:
                miss = miss +1 #If valid bit is 1 and the tag is different, we have a conflict miss
                cm[cmIndex]['tag'] = binary[:-des-index] #Update the tag
                cm[cmIndex]['val'] = 1 # Update the valid bit
                if dataGrid != None:
                    item = dataGrid.item(cmIndex,0)
                    item.setBackground(QColor("green"))
                    item.setText(binary[:-des-index])
                
                if checkCache(cm) == False: #Check if the cache is full
                    capacityMiss = capacityMiss + 1
                else:
                    conflictMiss = conflictMiss + 1

        else: # If the valid bit is 0, we have a compulsory miss
            miss = miss + 1
            compulsoryMiss = compulsoryMiss + 1
            cm[cmIndex]['tag'] = binary[:-des-index] #Update the tag
            cm[cmIndex]['val'] = 1 # Update the valid bit
            if dataGrid != None:
                item = dataGrid.item(cmIndex,0)
                item.setBackground(QColor("green"))
                item.setText(binary[:-des-index])
    
    #Writes the Cache Memory current state on the file
    with open('CacheReport.txt', 'w') as f:
        for key, value in cm.items():
            f.write('%s:%s\n' % (key, value))
    
    misses = round(miss/len(memoryAcess), 3)
    hits = round(hit/len(memoryAcess), 3)
    compulsoryMiss = round(compulsoryMiss/miss, 3)
    capacityMiss = round(capacityMiss/miss, 3)
    conflictMiss = round(conflictMiss/miss, 3)

    print("\n[Cache Simulation]")   
    if int(outputFlag) == 0:
        print(f'Hit:{hit}\t Miss:{miss}\t TotalAccess:{hit+miss}')
        print(f'HitRate:{hits}\t MissCompulsory:{compulsoryMiss}\t MissConflict:{conflictMiss}\t MissCapacity:{capacityMiss}\t')
        return f'{hit+miss}, {hits}, {misses}, {compulsoryMiss}, {capacityMiss}, {conflictMiss}'
    else:
        print(f'{hit+miss} {hits} {misses} {compulsoryMiss} {capacityMiss} {conflictMiss}')
        return f'{hit+miss} {hits} {misses} {compulsoryMiss} {capacityMiss} {conflictMiss}'

# Return: If outputflag = 0 return data + print , If outputflag = 1 return data
def cacheAssociativeMapAccess(DirectMap, replacementPolicy, memoryAcess, outputFlag, dataGrid):
    cl = DirectMap.cacheLines # cl = cache lines
    cm = [startCache(cl) for i in range(DirectMap.associativeWays)] # Construct a CacheMemory for each way of the cache, a cache memory is a dict and start evertything as 0 
    des = DirectMap.des # des = displacement
    index = DirectMap.index # size of cache index in bits

    hit = 0
    miss = 0
    compulsoryMiss = 0
    capacityMiss = 0
    conflictMiss = 0

    fifoV = fifo()
    lruV = lru()

    #each 32 bits on the file is a memory acess in binary 
    for binary in memoryAcess:
        #Gets the index of the binary
        if des == 0:
            cmIndex = int(binary[32-index:],2)
        else:
            if index == 0:
                cmIndex = 0
            else:
                cmIndex = int(binary[32-des-index:-des],2)
        isTagTrue = False
        #For each way j of the cache, we check if the tag is the same as the binary on the right position and check the valid bit
        for j in range(DirectMap.associativeWays):
            if  cm[j][cmIndex]['val'] == 1:
                #If the tag is the same, we have a hit
                if  cm[j][cmIndex]['tag'] == binary[:-des-index]:
                    hit = hit + 1
                    isTagTrue = True
                    if replacementPolicy == "L":
                        lruV.addToDict(cm[j][cmIndex]['tag'])
                    break
        #If the tag is not the same, we have a miss
        if isTagTrue == False:
            miss = miss + 1
            choosePosition = False
            #For each way j of the cache, we check if the valid bit is 0, if it is 0, we can use this way to store the new tag
            for j in range(DirectMap.associativeWays):
                if  cm[j][cmIndex]['val'] == 0:
                    compulsoryMiss = compulsoryMiss + 1
                    cm[j][cmIndex]['tag'] = binary[:-des-index]
                    cm[j][cmIndex]['val'] = 1

                    if replacementPolicy == "F":
                        fifoV.enqueue(cm[j][cmIndex]['tag'])
                    elif replacementPolicy == "L":
                        lruV.addToDict(cm[j][cmIndex]['tag'])

                    if dataGrid != None:
                        item = dataGrid.item(cmIndex,j)
                        item.setBackground(QColor("green"))
                        item.setText(binary[:-des-index])
                        
                    choosePosition = True
                    break
            #If choosePosition is false, it means that all the ways are full, so we need to use the replacement policy to choose which way to replace
            if choosePosition == False:
                if replacementPolicy == "R":
                    #Randomly choose a way to replace
                    addRandom = int(random.randrange(0, DirectMap.associativeWays)) 
                    #Check if the cache is full
                    isCmFull = True
                    for j in range(DirectMap.associativeWays):
                        if checkCache(cm[j]) == False:
                            isCmFull = False
                        
                    if isCmFull == True:
                        capacityMiss = capacityMiss + 1
                    else:
                        conflictMiss = conflictMiss + 1
                    
                    cm[addRandom][cmIndex]['tag'] = binary[:-des-index]
                    cm[addRandom][cmIndex]['val'] = 1
                    if dataGrid != None:
                        item = dataGrid.item(cmIndex,addRandom)
                        item.setBackground(QColor("green"))
                        item.setText(binary[:-des-index])

                elif replacementPolicy == "F":
                    Mylist = []
                    for i in range(DirectMap.associativeWays):
                        Mylist.append(cm[i][cmIndex]['tag'])
                    
                    addRandom = fifoV.checkWhoCameFirst(Mylist) 

                    #Check if the cache is full
                    isCmFull = True
                    for j in range(DirectMap.associativeWays):
                        if checkCache(cm[j]) == False:
                            isCmFull = False
                        
                    if isCmFull == True:
                        capacityMiss = capacityMiss + 1
                    else:
                        conflictMiss = conflictMiss + 1
                    
                    cm[addRandom][cmIndex]['tag'] = binary[:-des-index] # type: ignore
                    cm[addRandom][cmIndex]['val'] = 1 # type: ignore

                    fifoV.enqueue(cm[addRandom][cmIndex]['tag']) # type: ignore 

                    if dataGrid != None:
                        item = dataGrid.item(cmIndex,addRandom)
                        item.setBackground(QColor("green"))
                        item.setText(binary[:-des-index])     

                elif replacementPolicy == "L":
                    Mylist = []
                    for i in range(DirectMap.associativeWays):
                        Mylist.append(cm[i][cmIndex]['tag'])
                    
                    addRandom = lruV.checkWhoCameFirst(Mylist) 
                    
                    #Check if the cache is full
                    isCmFull = True
                    for j in range(DirectMap.associativeWays):
                        if checkCache(cm[j]) == False:
                            isCmFull = False
                        
                    if isCmFull == True:
                        capacityMiss = capacityMiss + 1
                    else:
                        conflictMiss = conflictMiss + 1
                    
                    cm[addRandom][cmIndex]['tag'] = binary[:-des-index] # type: ignore
                    cm[addRandom][cmIndex]['val'] = 1 # type: ignore
                    lruV.setItemToZero(cm[addRandom][cmIndex]['tag'])
                    lruV.addToDict(cm[addRandom][cmIndex]['tag']) # type: ignore 

                    if dataGrid != None:
                        item = dataGrid.item(cmIndex,addRandom)
                        item.setBackground(QColor("green"))
                        item.setText(binary[:-des-index])     
 
    with open('CacheReport.txt', 'w') as f:
        for i in range(DirectMap.associativeWays):
            f.write(f'Way {i+1}: \n')
            for key, value in cm[i].items():
                f.write('%s:%s\n' % (key, value))

    misses = round(miss/len(memoryAcess), 3)
    hits = round(hit/len(memoryAcess), 3)
    compulsoryMiss = round(compulsoryMiss/miss, 2)
    capacityMiss = round(capacityMiss/miss, 3)
    conflictMiss = round(conflictMiss/miss, 3)

    print("\n[Cache Simulation]")   
    if int(outputFlag) == 0:
        print(f'Hit:{hit}\t Miss:{miss}\t TotalAccess:{hit+miss}')
        print(f'HitRate:{hits}\t MissCompulsory:{compulsoryMiss}\t MissConflict:{conflictMiss}\t MissCapacity:{capacityMiss}\t')
        return f'{hit+miss} {hits} {misses} {compulsoryMiss} {capacityMiss} {conflictMiss}'
    else:
        print(f'{hit+miss} {hits} {misses} {compulsoryMiss} {capacityMiss} {conflictMiss}')
        return f'{hit+miss} {hits} {misses} {compulsoryMiss} {capacityMiss} {conflictMiss}'