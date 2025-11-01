/******************************************************************************
 *  Author       : Sanjeet Prasad
 *  Email        : sanjeet8.23@gmail.com
 *  Description  : Huffman File Compression and Decompression
 *                 - Compresses any binary/text file using Huffman coding
 *                 - Supports future extension to other formats (e.g., .docx, .pptx)
 *  Date         : 22-10-2025
 *  Language     : C (GCC)
 ******************************************************************************/

#ifndef HUFFMAN_H
#define HUFFMAN_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

// ==============================
// Struct Definitions
// ==============================

typedef struct HuffmanNode {
    uint8_t data;               // Byte value (0–255)
    unsigned freq;              // Frequency count
    struct HuffmanNode *left;   // Left child
    struct HuffmanNode *right;  // Right child
} HuffmanNode;

typedef struct MinHeap {
    unsigned size;              // Current heap size
    unsigned capacity;          // Max capacity
    HuffmanNode **array;        // Array of node pointers
} MinHeap;

typedef struct {
    int arr[256];               // Bit sequence
    int top;                    // Length of code
} HuffmanCode;

// ==============================
// Compression API
// ==============================

HuffmanNode* create_node(uint8_t data, unsigned freq);
MinHeap* create_min_heap(unsigned capacity);
void build_min_heap(MinHeap* heap);
void insert_min_heap(MinHeap* heap, HuffmanNode* node);
HuffmanNode* extract_min(MinHeap* heap);
HuffmanNode* build_huffman_tree(uint8_t data[], int freq[], int size);
void store_codes(HuffmanNode* root, int arr[], int top, HuffmanCode codes[]);

// ==============================
// File I/O Utilities
// ==============================

void compress_file(const char* input_file, const char* output_file);
void decompress_file(const char* input_file, const char* output_file);
long file_size(const char* filename);
void preview_bytes(const char* filename, int count);

// ==============================
// Future Extension Hooks
// ==============================

bool is_supported_file(const char* filename); // Placeholder for file type detection
void log_message(const char* tag, const char* message); // Logging macro

#endif // HUFFMAN_H
