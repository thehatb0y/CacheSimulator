from ast import Str
import math
from random import random

class CacheConfig():
    def __init__(self, cs, ba, bs, ma, aw):
        #Cache size for 64KB
        self.cacheSize = cs * 1024# Convert to first argument into KB, 32 = 32KB, 64 = 64KB, 128 = 128KB, 256 = 256KB
        self.byteAddress = ba # 8 bits = 1 byte
        self.blockSize =  bs # 8 bits = 1 byte
        self.memoryAddressSize = ma # 32 or 64 bits
        self.associativeWays = aw # 1 = Direct Mapping, 2 = 2-way associative, 4 = 4-way associative, 8 = 8-way associative, 16 = 16-way associative
        
        self.cacheLines = int((self.cacheSize/(self.blockSize/self.byteAddress)/self.associativeWays)) #Cache index size
        self.index = int(math.log(self.cacheLines,2)) # number of bits for index
        self.des = int(math.log(self.blockSize/self.byteAddress,2)) # number of bits for des
        self.trueCacheSize = int(((self.cacheLines*self.associativeWays) * (self.blockSize + (self.memoryAddressSize-self.index-self.des)+1))/8192) # Conversion for true cache size in KB 
        
        print(f'CacheSize:{int(self.cacheSize/1024)}KB\t TrueCacheSize: {self.trueCacheSize}KB\t Index: {self.index}Bits\t Tag:{self.memoryAddressSize-self.index-self.des}\t Des:{self.des}')
        print(f'BlockSize:{int(self.blockSize/8)}B\t ByteAddress: {int(self.byteAddress/8)}B\t MemoryAddressSize: {self.memoryAddressSize}Bits')

def startCache(cl):
    #create a disct of cache lines and insert tag = 0 , val = 0 , data = 0 in range of cache lines
    cacheMemory = {}
    for i in range(cl):
        cacheMemory[i] = {'tag':0,'val':0,'data':0}
    return cacheMemory

def cacheDirectMapAccess(DirectMap, an):
    cl = DirectMap.cacheLines
    cm = startCache(cl)
    des = DirectMap.des
    index = DirectMap.index

    hit = 0
    miss = 0
    ramSize = DirectMap.cacheSize * 8 # RamSize is 8 times the cache size

    for i in range(an):
        #set address as a random from 0 to ramSize
        address = int(random() * ramSize)

        #convert address to binary
        binary = bin(address)
        if  cm[address%cl]['val'] == 1:
            if  cm[address%cl]['tag'] == binary[:-des-index]:
                hit = hit + 1
            else:
                miss = miss +1
        else:
            miss = miss +1
            cm[address%cl]['tag'] = binary[:-des-index]
            cm[address%cl]['val'] = 1
            cm[address%cl]['data'] = binary
    print(f'Hit:{hit}\t Miss:{miss}\t HitRate:{hit/an*100}%\t Hit+Miss:{hit+miss}')

def cacheAssociativeMapAccess(DirectMap, an, aw):
    cl = DirectMap.cacheLines
    des = DirectMap.des
    index = DirectMap.index

    hit = 0
    miss = 0
    ramSize = DirectMap.cacheSize * 8 # RamSize is 8 times the cache size
    #create a list of cacheMemory, the list have size of associativeWays and each item from the list should call startCache function
    cm = [startCache(cl) for i in range(aw)]

    a =0
    #check check if tag = 0 in each cm list
    for i in range(an):
        #set address as a random from 0 to ramSize
        address = int(random() * ramSize)
        #convert address to binary
        binary = bin(address)
        count = 0
        a= a+1
        for j in range(aw):
            count = count + 1
            if  cm[j][address%cl]['val'] == 1:
                if  cm[j][address%cl]['tag'] == binary[:-des-index]:
                    hit = hit + 1
                    break
        if count == aw and cm[count-1][address%cl]['tag'] != binary[:-des-index]:
            miss = miss +1
            addRandom = int(random() * aw)
            cm[addRandom][address%cl]['tag'] = binary[:-des-index]
            cm[addRandom][address%cl]['val'] = 1
            cm[addRandom][address%cl]['data'] = binary       

    print(f'Hit:{hit}\t Miss:{miss}\t HitRate:{hit/an*100}%\t Hit+Miss:{hit+miss}')
