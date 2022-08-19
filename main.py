import cache

def main():

    cacheSize = 64# Convert to first argument into KB, 32 = 32KB, 64 = 64KB, 128 = 128KB, 256 = 256KB
    byteAddress = 8 # 8 bits = 1 byte
    blockSize =  32 # 8 bits = 1 byte
    memoryAddressSize = 32 # 32 or 64 bits
    associativeWays = 1 # 1 = Direct Mapping, 2 = 2-way associative, 4 = 4-way associative, 8 = 8-way associative, 16 = 16-way associative
    accessNumber = 1000000 # Number of accesses for simulation

    DirectMap = cache.CacheConfig(cacheSize, byteAddress, blockSize, memoryAddressSize, associativeWays)
    cacheMemory = cache.startCache(DirectMap.cacheLines)
    cache.cacheDirectMapAccess(DirectMap, cacheMemory, accessNumber)

    AssociativeMap16way = cache.CacheConfig(cacheSize, byteAddress, blockSize, memoryAddressSize, 16)
    cache.cacheAssociativeMapAccess(AssociativeMap16way, accessNumber, 16)

if __name__ == "__main__":
    main()