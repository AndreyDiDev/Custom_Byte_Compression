// Author : Andrey Dimanchev
// Version: Final
#include <stdio.h>


/**
 * Set most significant bit of a byte to 1.
 */
unsigned char set_msb(unsigned char byte) {
    return byte | 0x80;
}
/**
 * Compresses a byte array by replacing sequences of the same byte with a single byte and a count.
 */
int byte_compress(unsigned char *data_ptr, int data_size) {
    unsigned char compressed_data[data_size * 2];
    int compressed_size = 0;
    
    int i = 0;
    while (i < data_size) {
        unsigned char byte = data_ptr[i];
        int count = 1;
        
        while (i + count < data_size && data_ptr[i + count] == byte && count < 127) {
            count++;
        }
        
        if(count == 1) {
            byte = set_msb(byte);
            compressed_data[compressed_size++] = byte;
            compressed_data[compressed_size++] = count;
        }
        else {
            compressed_data[compressed_size++] = byte;
            compressed_data[compressed_size++] = count;
        }
        
        i += count;
    }
    
    // Copy compressed data back to original buffer
    for (int j = 0; j < compressed_size; j++) {
        data_ptr[j] = compressed_data[j];
    }
    
    return compressed_size;
}

/**
 * Decompress a byte array that was compressed using the byte_compress function.
 */
int byte_decompress(unsigned char *data_ptr, int data_size) {
    unsigned char decompressed_data[data_size * 2];
    int decompressed_size = 0;
    
    int i = 0;
    while (i < data_size) {
        unsigned char byte = data_ptr[i];
        if((byte & 0x80) == 0) {
            decompressed_data[decompressed_size++] = byte;
            i++;
            continue;
        }
        
        int count = data_ptr[i + 1];
        
        for (int j = 0; j < count; j++) {
            decompressed_data[decompressed_size++] = byte;
        }
        
        i += 2;
    }
    
    // Copy decompressed data back to original buffer
    for (int j = 0; j < decompressed_size; j++) {
        data_ptr[j] = decompressed_data[j];
    }
    
    return decompressed_size;
}


/**
 * Main function to test the byte_compress function.
 */
int main() {
    unsigned char data[] = { 0x03, 0x74, 0x04, 0x04, 0x04, 0x35, 0x35, 0x64,
                             0x64, 0x64, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00,
                             0x56, 0x45, 0x56, 0x56, 0x56, 0x09, 0x09, 0x09 };
    int data_size = 24;
    
    int new_size = byte_compress(data, data_size);

    printf("Original data: ");
    for (int i = 0; i < data_size; i++) {
        printf("%x ", data[i]);
    }

    printf("\n");
    
    printf("Compressed data: ");
    for (int i = 0; i < new_size; i++) {
        printf("%x ", data[i]);
    }
    printf("\nNew size: %d\n", new_size);

    new_size = byte_decompress(data, new_size);

    printf("Decompressed data: ");
    for (int i = 0; i < new_size; i++) {
        printf("%x ", data[i]);
    }

    // assert they are equal
    for (int i = 0; i < data_size; i++) {
        if (data[i] != data[i]) {
            printf("Error: decompressed data does not match original data\n");
            return 1;
        }
    }

    printf("\nDecompressed data matches original data\n");

    return 0;
}
