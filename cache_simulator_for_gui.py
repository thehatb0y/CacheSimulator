import cache

def cache_sim(nsets, blockSize, associativity, replacementPolicy, outputFlag, inputFile, dataGride):
    byteAddress = 8 
    memoryAcess = []

    #read the file and convert to a dict structure with binary numbers
    try :
        file = open(f'{inputFile}.bin', "rb")
    except FileNotFoundError:
        print("File not found")
        return None

    data = file.read() # the file read comes into hexadecimal format, so data = hexadecimal
    binary = bin(int.from_bytes(data, byteorder='big')) # then we convert to binary
    
    # when we convert the file to binary, the first number is 0b, so we need remove it and add 0 to the left, that just happens on the first word
    first_word_bin = bin(int.from_bytes(data[:4], byteorder='big')) # first word = 4 bytes
    n = (32-len(first_word_bin[2:])) # remove the 0b
    first_word = ("0"*n)+first_word_bin[2:] # count the number of 0 to add to the left
    memoryAcess.append(str(first_word)) # add the first word to the list

    i = len(first_word_bin) # i is the number of bits of the first word

    while binary[i:i+32] != "": # start from i and go to the end of the file
        memoryAcess.append(str(binary[i:i+32]))
        i = i + 32

    if associativity == 1:
            return cache.cacheDirectMapAccess(cache.CacheConfig(nsets, blockSize, associativity, byteAddress), memoryAcess, outputFlag, dataGride)
    elif associativity > 1 and associativity%2 == 0:
            return cache.cacheAssociativeMapAccess(cache.CacheConfig(nsets, blockSize, associativity, byteAddress), replacementPolicy, memoryAcess, outputFlag, dataGride)
    else:
        print("Invalid Associative-Way")
        exit()
