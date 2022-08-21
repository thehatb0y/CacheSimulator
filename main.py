import cache
import matplotlib.pyplot as plt

def main():

    cacheSize = 64# Convert to first argument into KB, 32 = 32KB, 64 = 64KB, 128 = 128KB, 256 = 256KB
    byteAddress = 8 # 8 bits = 1 byte
    blockSize =  32 # 8 bits = 1 byte
    memoryAddressSize = 32 # 32 or 64 bits
    associativeWays = 1 # 1 = Direct Mapping, 2 = 2-way associative, 4 = 4-way associative, 8 = 8-way associative, 16 = 16-way associative
    accessNumber = 1000000 # Number of accesses for simulation

    DirectMap = cache.CacheConfig(32, byteAddress, blockSize, memoryAddressSize, associativeWays)
    hitMap32 = cache.cacheDirectMapAccess(DirectMap, accessNumber)

    DirectMap = cache.CacheConfig(64, byteAddress, blockSize, memoryAddressSize, associativeWays)
    hitMap64 = cache.cacheDirectMapAccess(DirectMap, accessNumber)

    DirectMap = cache.CacheConfig(128, byteAddress, blockSize, memoryAddressSize, associativeWays)
    hitMap128 = cache.cacheDirectMapAccess(DirectMap, accessNumber)

    #AssociativeMap16way = cache.CacheConfig(32, byteAddress, blockSize, memoryAddressSize, 16)
    #hitAw16 = cache.cacheAssociativeMapAccess(AssociativeMap16way, accessNumber, 16)

    AssociativeMap16way = cache.CacheConfig(32, byteAddress, blockSize, memoryAddressSize, 16)
    hitAw1632 = cache.cacheAssociativeMapAccess(AssociativeMap16way, accessNumber, 16)

    AssociativeMap16way = cache.CacheConfig(64, byteAddress, blockSize, memoryAddressSize, 16)
    hitAw1664 = cache.cacheAssociativeMapAccess(AssociativeMap16way, accessNumber, 16)

    AssociativeMap16way = cache.CacheConfig(128, byteAddress, blockSize, memoryAddressSize, 16)
    hitAw16128 = cache.cacheAssociativeMapAccess(AssociativeMap16way, accessNumber, 16)

    #AssociativeMap16way = cache.CacheConfig(cacheSize, byteAddress, blockSize, memoryAddressSize, 8)
    #hitAw8 = cache.cacheAssociativeMapAccess(AssociativeMap16way, accessNumber, 8)

    #AssociativeMap16way = cache.CacheConfig(cacheSize, byteAddress, blockSize, memoryAddressSize, 4)
    #hitAw4 = cache.cacheAssociativeMapAccess(AssociativeMap16way, accessNumber, 4)

    #plot a graph hit rate vs cache size
    plt.plot([32 ,64, 128], [hitMap32, hitMap64, hitMap128], label = 'Direct Map')
    plt.plot([32 ,64, 128], [hitAw1632, hitAw1664, hitAw16128], label = 'Associative 16')

    plt.xlabel('Cache Size (KB)')
    plt.ylabel('Hit Rate (%)')
    plt.show()

if __name__ == "__main__":
    main()
