/******************************************************************************
 *  File         : huffman.c
 *  Author       : Sanjeet Prasad
 *  Email        : sanjeet8.23@gmail.com
 *  Description  : Core Huffman logic for file compression and decompression
 *                 - Implements heap operations, tree construction, and code storage
 *                 - Provides file utilities and extension hooks
 *                 - Designed for modularity and future format support (.txt, .docx, .pptx)
 *  Date         : 22-10-2025
 *  Language     : C (GCC)
 ******************************************************************************/

#include "../include/huffman.h"

// ==============================
// Node and Heap Operations
// ==============================

HuffmanNode* create_node(uint8_t data, unsigned freq) {
    HuffmanNode* node = (HuffmanNode*)malloc(sizeof(HuffmanNode));
    if (!node) return NULL;
    node->data = data;
    node->freq = freq;
    node->left = node->right = NULL;
    return node;
}

MinHeap* create_min_heap(unsigned capacity) {
    MinHeap* heap = (MinHeap*)malloc(sizeof(MinHeap));
    if (!heap) return NULL;
    heap->size = 0;
    heap->capacity = capacity;
    heap->array = (HuffmanNode**)malloc(capacity * sizeof(HuffmanNode*));
    return heap;
}

static void swap_nodes(HuffmanNode** a, HuffmanNode** b) {
    HuffmanNode* temp = *a;
    *a = *b;
    *b = temp;
}

static void min_heapify(MinHeap* heap, int idx) {
    int smallest = idx;
    int left = 2 * idx + 1;
    int right = 2 * idx + 2;

    if (left < heap->size && heap->array[left]->freq < heap->array[smallest]->freq)
        smallest = left;
    if (right < heap->size && heap->array[right]->freq < heap->array[smallest]->freq)
        smallest = right;

    if (smallest != idx) {
        swap_nodes(&heap->array[smallest], &heap->array[idx]);
        min_heapify(heap, smallest);
    }
}

void build_min_heap(MinHeap* heap) {
    for (int i = (heap->size - 1) / 2; i >= 0; --i)
        min_heapify(heap, i);
}

void insert_min_heap(MinHeap* heap, HuffmanNode* node) {
    int i = heap->size++;
    while (i && node->freq < heap->array[(i - 1) / 2]->freq) {
        heap->array[i] = heap->array[(i - 1) / 2];
        i = (i - 1) / 2;
    }
    heap->array[i] = node;
}

HuffmanNode* extract_min(MinHeap* heap) {
    HuffmanNode* temp = heap->array[0];
    heap->array[0] = heap->array[--heap->size];
    min_heapify(heap, 0);
    return temp;
}

// ==============================
// Huffman Tree and Code Storage
// ==============================

HuffmanNode* build_huffman_tree(uint8_t data[], int freq[], int size) {
	
	if (size <= 0 || data == NULL || freq == NULL) {
    return NULL;
	}
    MinHeap* heap = create_min_heap(size);
    for (int i = 0; i < size; ++i)
        heap->array[i] = create_node(data[i], freq[data[i]]);
    heap->size = size;
    build_min_heap(heap);

    while (heap->size > 1) {
        HuffmanNode* left = extract_min(heap);
        HuffmanNode* right = extract_min(heap);
        HuffmanNode* top = create_node('$', left->freq + right->freq);
        top->left = left;
        top->right = right;
        insert_min_heap(heap, top);
    }

    return extract_min(heap);
}

void store_codes(HuffmanNode* root, int arr[], int top, HuffmanCode codes[]) {
    if (root->left) {
        arr[top] = 0;
        store_codes(root->left, arr, top + 1, codes);
    }
    if (root->right) {
        arr[top] = 1;
        store_codes(root->right, arr, top + 1, codes);
    }
    if (!root->left && !root->right) {
        codes[root->data].top = top;
        for (int i = 0; i < top; ++i)
            codes[root->data].arr[i] = arr[i];
    }
}

// ==============================
// File Utilities
// ==============================

long file_size(const char* filename) {
    FILE* f = fopen(filename, "rb");
    if (!f) return -1;
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fclose(f);
    return size;
}

void preview_bytes(const char* filename, int count) {
    FILE* f = fopen(filename, "rb");
    if (!f) return;
    printf("Preview of %s:\n", filename);
    for (int i = 0; i < count; ++i) {
        uint8_t ch;
        if (fread(&ch, 1, 1, f) != 1) break;
        printf("%02X ", ch);
    }
    printf("\n\n");
    fclose(f);
}

// ==============================
// Compression and Decompression
// ==============================

void compress_file(const char* input_file, const char* output_file) {
    FILE* in = fopen(input_file, "rb");
    FILE* out = fopen(output_file, "wb");
    if (!in || !out) {
        log_message("ERROR", "Error opening files!");
        return;
    }

    int freq[256] = {0};
    unsigned char ch;
    while (fread(&ch, 1, 1, in) == 1)
        freq[ch]++;

    uint8_t data[256];
    int size = 0;
    for (int i = 0; i < 256; ++i)
        if (freq[i] > 0) data[size++] = (uint8_t)i;

    if (size == 0) {
        fclose(in);
        fclose(out);
        return;
    }

    HuffmanNode* root = build_huffman_tree(data, freq, size);
    HuffmanCode codes[256] = {0};
    int arr[256];
    store_codes(root, arr, 0, codes);

    for (int i = 0; i < 256; ++i)
        fwrite(&freq[i], sizeof(int), 1, out);

    rewind(in);
    unsigned char buffer = 0;
    int bits = 0;
    while (fread(&ch, 1, 1, in) == 1) {
        for (int i = 0; i < codes[ch].top; ++i) {
            buffer = (buffer << 1) | codes[ch].arr[i];
            if (++bits == 8) {
                fwrite(&buffer, 1, 1, out);
                bits = 0;
                buffer = 0;
            }
        }
    }
    if (bits > 0) {
        buffer <<= (8 - bits);
        fwrite(&buffer, 1, 1, out);
    }

    fclose(in);
    fclose(out);
    free(root);
}

void decompress_file(const char* input_file, const char* output_file) {
    FILE* in = fopen(input_file, "rb");
    FILE* out = fopen(output_file, "wb");
    if (!in || !out) {
        log_message("ERROR", "Error opening files!");
        return;
    }

    int freq[256] = {0};
    for (int i = 0; i < 256; ++i)
        fread(&freq[i], sizeof(int), 1, in);

    uint8_t data[256];
    int size = 0;
    for (int i = 0; i < 256; ++i)
        if (freq[i] > 0) data[size++] = (uint8_t)i;

    HuffmanNode* root = build_huffman_tree(data, freq, size);
    HuffmanNode* current = root;

    // Calculate total number of original bytes
    long original_size = 0;
    for (int i = 0; i < 256; ++i)
        original_size += freq[i];

    long written = 0;
    unsigned char buffer;
    while (fread(&buffer, 1, 1, in) == 1 && written < original_size) {
        for (int i = 7; i >= 0; --i) {
            int bit = (buffer >> i) & 1;
            current = bit ? current->right : current->left;
            if (!current->left && !current->right) {
                fputc(current->data, out);
                current = root;
                if (++written >= original_size) break;
            }
        }
    }

    fclose(in);
    fclose(out);
    free(root);
}
// ==============================
// Future Extension Hooks
// ==============================

bool is_supported_file(const char* filename) {
    // Placeholder: check extension or magic bytes
    return true;
}

void log_message(const char* tag, const char* message) {
    printf("[%s] %s\n", tag, message);
}
