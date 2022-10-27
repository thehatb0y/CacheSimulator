import cache
import matplotlib.pyplot as plt

#cache_simulator <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada
    #cacheSize = 64 # in KB 1= 1KB, 64 = 64KB
    #byteAddress = 8 # 8 bits = 1 byte
    #blockSize =  32 # 8 bits = 1 byte
    #memoryAddressSize = 32 # 32 or 64 bits
    #associativeWays = 1 # 1 = Direct Mapping, 2 = 2-way associative, 4 = 4-way associative, 8 = 8-way associative, 16 = 16-way associative
#nsets, blockSize, associativity, replacementPolicy, outputFlag, inputFile

def main():
    #cache_simulator <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada

    nsets = 256
    blockSize = 32
    associativity = 1
    byteAddress = 8 

    replacementPolicy = "r"
    outputFlag = "a"

    inputFile =  "bin_100"
    memoryAcess = []
    with open(f'{inputFile}.txt', 'r') as txt:
        for line in txt:
            memoryAcess.append(int(line))
    
    if associativity == 1:
            cache.cacheDirectMapAccess(cache.CacheConfig(nsets, blockSize, associativity, byteAddress), memoryAcess)
    elif associativity > 1:
            cache.cacheAssociativeMapAccess(cache.CacheConfig(nsets, blockSize, associativity, byteAddress), memoryAcess)
    else:
        print("Invalid Associative-Way")
        exit()

if __name__ == "__main__":
    main()
