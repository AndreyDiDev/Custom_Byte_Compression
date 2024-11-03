# Author: Andrey Dimanchev
# Version: Final

# Description: This file contains the functions that will be used to compress and decompress data
def set_msb_to_one(num):
    # Assuming an 8-bit number
    return num | 0b10000000

# Set the most significant bit to zero
def set_msb_to_zero(num):
    return num & 0b01111111

# get the most significant bit index
def get_msb_index(num):
    bit_length = num.bit_length()  # Get the bit length of the number
    msb_index = bit_length - 1  # Index of the MSB
    return msb_index

# compress function with type2 compression (Refer to doc)
def compress_type2(data):
    n = len(data)
    bytesDone = []
    i = 0
    # print("i: ", i)
    
    # store final output
    compressedData = []
    
    # run through all bytes
    while i < n:
        # reset for each byte
        endsIndices = []
        byte = data[i]

        # print("byte at i: ", byte)
        
        # check for already done bytes and skip over them
        while(byte in bytesDone and i < n):
            byte = data[i]
            i += 1
            
        j = i
        
        # check if at current we have a run
        running = False
        while(j < n and data[j] == byte):
            j += 1
            # print("j: ", j)
            # print("considering at j byte: ", data[j])
            running = True
            
        if(running):
            endsIndices.append(j)
        # ------------------------
        
        # put pointer to the end of the current run
        i = j
        
        # print("scanning for other runs of the same byte", byte)
        # scan for other runs of the same byte
        while(j < n):
            # found another run after the current run
            if(byte == data[j]):
                k = j + 1
                while(k < n and data[k] == byte):
                    k += 1
                j = k
                endsIndices.append(k)
            j += 1

        # print("endsIndices: ", endsIndices)
        
        # finished all runs
        if(byte not in bytesDone):
            # print("byte not in bytesDone: ", byte)
            # by default we assume byte is dont running
            bytesDone.append(byte)
            if(len(endsIndices) <= 1):
                # print("single-run byte: ", byte)
                # single-run byte
                compressedData.append(byte)
            elif(len(endsIndices) < 256):
                # print("multi-run byte: ", byte)
                # multi-run byte
                byte = set_msb_to_one(byte)
                compressedData.append(byte)
                compressedData.append(len(endsIndices))
                # append individual indices
                for x in endsIndices:
                    compressedData.append(x)
            else:
                byte = set_msb_to_one(byte)
                # if more than 256 runs, we need to split the runs
                # reset its possible to have more than 256 runs
                compressedData.append(byte)
                compressedData.append(len(endsIndices))
                for x in endsIndices:
                    compressedData.append(x)
        
        # print("finised byte: ", byte)
        # print("compressedData : ", compressedData)
        # move to next byte
        # i += 1    
        
    return compressedData

# Convert data to bytearray
def convert_to_bytearray(data):
    return bytearray(data)

# compress function with type1 compression (Refer to doc)
def compress(data):
    n = len(data)
    i = 0
    compressedData = []
    
    while i < n:
        byte = data[i]
        
        k = 0
        while i < n and data[i] == byte and k < 255:
            k += 1
            i += 1

        if(k == 0):
            compressedData.append(byte)
        else:
            byte = set_msb_to_one(byte)
            compressedData.append(byte)
            compressedData.append(k)
    
    return compressedData

# where format of data is [(byte, [indices]), ...] and assume 
# To note: Was not able to fully finish this function
# Refer to documentation for more information on its implementation
def decompress_type2(data, originalSize):
    # initialize with original size
    decompressedData = bytearray(originalSize)
    # print("len decompressedData: ", len(decompressedData))
    prevByteIndex = 0

    for i in range(len(data)):
        # assumes i is pointing and will be
        # pointing to a byte of actual number by this line
        # print("decompressedData: ", decompressedData)
        byte = data[i]
        if(get_msb_index(byte) == 0):
            # single byte run
            decompressedData.append(byte)
            i += 1
        else:
             # Multi-byte run
            runLength = data[i + 1]
            # insert at lowest filled index

            decompressedData[i] = set_msb_to_zero(byte)
            indices = data[i + 2:i + 2 + runLength-1]
            for index in indices:
                # print("byte: ", byte)
                # print("index: ", index)
                decompressedData[index] = set_msb_to_zero(byte)

            i += 2 + runLength

        # find bytePrev's smallest index
        prevByteIndex = indices[0]

    return decompressedData

# compress function that will return the smallest compressed data
# if both compressed data are the same size, return Type 1 compressed data
def compressFunction(data):
    type2_CompressedData = compress_type2(data)
    type1_CompressedData = compress(data)

    if(len(type2_CompressedData) < len(type1_CompressedData)):
        return type2_CompressedData
    elif(len(type2_CompressedData) > len(type1_CompressedData)):
        return type1_CompressedData
    elif(len(type2_CompressedData) == len(type1_CompressedData)):
        return type1_CompressedData

# decompress function that will return the decompressed data
# automatically knows which type of compression is used
def decompressFunction(data, originalSize):
    type2_DecompressedData = decompress_type2(data, originalSize)
    type1_DecompressedData = decompress_type1(data, originalSize)

    # if both decompressed data are the same size, return Type 1 decompressed data
    if(len(type2_DecompressedData) == len(type1_DecompressedData)):
        return type1_DecompressedData
    # decide which decompressed data to return
    elif(len(type2_DecompressedData) == originalSize):
        return type2_DecompressedData
    elif(len(type1_DecompressedData) == originalSize):
        return type1_DecompressedData
    
# decompress function with type1 compression (Refer to doc)
def decompress_type1(data, originalSize):
    decompressedData = bytearray(originalSize)
    i = 0

    while i < len(data):
        byte = data[i]
        if(get_msb_index(byte) == 0):
            decompressedData.append(byte)
            i += 1
        else:
            runLength = data[i + 1]
            byte = set_msb_to_zero(byte)
            for j in range(runLength):
                decompressedData.append(byte)
            i += 2

    return decompressedData

# test
data = [1, 1, 1, 3, 2, 2, 2, 3, 3, 3, 4, 4, 4,1, 1, 1, 1,2,2,1,2,5]
print("original data: ", convert_to_bytearray(data))
# compressedData = compress_type2(data)
# print("2compressed size: ", len(compressedData))
# print(compressedData)
# print("byteArray: ", convert_to_bytearray(compressedData))

# compressedDataType1 = compress(data)
# print("compressedType1Data: ", compressedDataType1)
# print("byteArray: ", convert_to_bytearray(compressedDataType1))
# print("len of Type1 compressed data: ", len(compressedDataType1))

finalCompressedData = compressFunction(data)
# print("finalCompressedData: ", finalCompressedData)
print("compressed: ", convert_to_bytearray(finalCompressedData))
print("original size: ", len(data))
print("compressed size: ", len(finalCompressedData))

# decompressedData = decompress_type2(convert_to_bytearray(compress_type2(data)), len(data))
# print(decompressedData)
