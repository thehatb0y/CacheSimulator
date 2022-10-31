import cache
import sys

#cache_simulator <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada
    #cacheSize = 64 # in KB 1= 1KB, 64 = 64KB
    #byteAddress = 8 # 8 bits = 1 byte
    #blockSize =  32 # 8 bits = 1 byte
    #memoryAddressSize = 32 # 32 or 64 bits
    #associativeWays = 1 # 1 = Direct Mapping, 2 = 2-way associative, 4 = 4-way associative, 8 = 8-way associative, 16 = 16-way associative

# how to run:
#           python main.py 256 4 1 R 1 bin_100
#           python main.py 128 2 4 R 1 bin_1000
#           python main.py 256 1 2 R 1 bin_10000

def main():
    nsets = int(sys.argv[1])
    blockSize = int(sys.argv[2])*8
    associativity = int(sys.argv[3])
    byteAddress = 8 

    replacementPolicy = str(sys.argv[4])
    outputFlag = int(sys.argv[5])

    inputFile =  str(sys.argv[6])
    memoryAcess = []

    file = open(f'{inputFile}.bin', "rb")
    data = file.read()

    binary = bin(int.from_bytes(data, byteorder='big'))
    first_word_bin = bin(int.from_bytes(data[:4], byteorder='big'))

    n = (32-len(first_word_bin[2:]))
    first_word = ("0"*n)+first_word_bin[2:]
    memoryAcess.append(str(first_word))
    i = len(first_word_bin)
    total = 0

    while binary[i:i+32] != "":
        memoryAcess.append(str(binary[i:i+32]))
        i = i + 32
        total = total + 1

    if associativity == 1:
            return cache.cacheDirectMapAccess(cache.CacheConfig(nsets, blockSize, associativity, byteAddress), memoryAcess, outputFlag)
    elif associativity > 1:
            return cache.cacheAssociativeMapAccess(cache.CacheConfig(nsets, blockSize, associativity, byteAddress), memoryAcess, outputFlag)
    else:
        print("Invalid Associative-Way")
        exit()

if __name__ == "__main__":
    main()
