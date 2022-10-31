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
    # cache_simulator 128 2 4 R 1 bin_1000.bin

    nsets = 256
    blockSize = 32
    associativity = 1
    byteAddress = 8 

    replacementPolicy = "r"
    outputFlag = "a"
    
    inputFile =  "bin_10000"
    memoryAcess = []

    file = open(f'{inputFile}.bin', "rb")
    data = file.read()

    binary = bin(int.from_bytes(data, byteorder='big'))
    first_word_bin = bin(int.from_bytes(data[:4], byteorder='big'))

    n = (32-len(first_word_bin[2:]))
    first_word = ("0"*n)+first_word_bin[2:]
    #memoryAcess.append(str(first_word))
    i = len(first_word_bin)
    total = 0

    while binary[i:i+32] != "":
        #memoryAcess.append(str(binary[i:i+32]))
        i = i + 32
        total = total + 1

    for i in range(50):
        memoryAcess.append(str(1))
        memoryAcess.append(str(100000001))

    if associativity == 1:
            cache.cacheDirectMapAccess(cache.CacheConfig(nsets, blockSize, associativity, byteAddress), memoryAcess)
    elif associativity > 1:
            cache.cacheAssociativeMapAccess(cache.CacheConfig(nsets, blockSize, associativity, byteAddress), memoryAcess)
    else:
        print("Invalid Associative-Way")
        exit()

if __name__ == "__main__":
    main()
