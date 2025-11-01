/******************************************************************************
 *  File         : test_huffman.c
 *  Author       : Sanjeet Prasad
 *  Email        : sanjeet8.23@gmail.com
 *  Description  : Unit tests for Huffman compression module using Unity framework
 *                 - Validates heap operations, tree construction, and code correctness
 *                 - Ensures compression-decompression fidelity for sample inputs
 *                 - Uses ./data/ folder for all test files
 *  Date         : 22-10-2025
 *  Language     : C (GCC)
 ******************************************************************************/

#include "../include/huffman.h"
#include "unity/unity.h"

int test_counter = 0;
extern struct UNITY_STORAGE_T Unity;

// Called before each test case
void setUp(void) {
    test_counter++;
    //printf("[TEST] [%d] Starting test: %s\n", test_counter, Unity.CurrentTestName);

}

// Called after each test case
void tearDown(void) {
    //printf("TEST [%d] Completed test: %s\n", test_counter, Unity.CurrentTestName);
}

// Test creation of a single Huffman node
void test_create_node(void) {
    HuffmanNode* node = create_node('A', 5);
    TEST_ASSERT_NOT_NULL(node);
    TEST_ASSERT_EQUAL_UINT8('A', node->data);
    TEST_ASSERT_EQUAL_UINT(5, node->freq);
    TEST_ASSERT_NULL(node->left);
    TEST_ASSERT_NULL(node->right);
    free(node);
}

// Test insertion and extraction from min heap
void test_min_heap_insert_extract(void) {
    MinHeap* heap = create_min_heap(3);
    insert_min_heap(heap, create_node('A', 5));
    insert_min_heap(heap, create_node('B', 2));
    insert_min_heap(heap, create_node('C', 8));

    HuffmanNode* min = extract_min(heap);
    TEST_ASSERT_EQUAL_UINT8('B', min->data); // 'B' has lowest frequency
    free(min);
    free(heap->array);
    free(heap);
}

// Test Huffman tree construction from frequency table
void test_huffman_tree_build(void) {
	int freq[256] = {0};
	freq['A'] = 5;
	freq['B'] = 2;	
	freq['C'] = 8;
	uint8_t data[] = {'A', 'B', 'C'};
	HuffmanNode* root = build_huffman_tree(data, freq, 3);
	TEST_ASSERT_NOT_NULL(root);
	TEST_ASSERT_EQUAL_UINT(15, root->freq);
	free(root);
}

// Test code generation from Huffman tree
void test_store_codes(void) {
    uint8_t data[] = {'A', 'B'};
    int freq[] = {1, 1};
    HuffmanNode* root = build_huffman_tree(data, freq, 2);
    HuffmanCode codes[256] = {0};
    int arr[256];
    store_codes(root, arr, 0, codes);
    TEST_ASSERT_TRUE(codes['A'].top > 0 || codes['B'].top > 0);
    free(root);
}

// Test full compression-decompression roundtrip on a sample file
void test_file_roundtrip(void) {
    const char* input = "data/test_input.txt";
    const char* compressed = "data/test_compressed.bin";
    const char* decompressed = "data/test_output.txt";

    // Step 1: Create sample input file
    FILE* f = fopen(input, "w");
    fprintf(f, "huffman compression test line\nhuffman compression test line\n");
    fclose(f);

    // Step 2: Compress and decompress
    compress_file(input, compressed);
    decompress_file(compressed, decompressed);

    // Step 3: Compare byte-by-byte
    FILE* f1 = fopen(input, "rb");
    FILE* f2 = fopen(decompressed, "rb");
    TEST_ASSERT_NOT_NULL(f1);
    TEST_ASSERT_NOT_NULL(f2);

    int ch1, ch2;
    while ((ch1 = fgetc(f1)) != EOF && (ch2 = fgetc(f2)) != EOF) {
        TEST_ASSERT_EQUAL_UINT8(ch1, ch2);
    }

    // Ensure both files ended at the same time
    TEST_ASSERT_EQUAL_INT(EOF, fgetc(f1));
    TEST_ASSERT_EQUAL_INT(EOF, fgetc(f2));

    fclose(f1);
    fclose(f2);
}

void test_invalid_tree_build(void) {
	HuffmanNode* root = build_huffman_tree(NULL, NULL, 0);
	TEST_ASSERT_NULL(root);
}

// Entry point for Unity test runner
int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_create_node);
    RUN_TEST(test_min_heap_insert_extract);
    RUN_TEST(test_huffman_tree_build);
    RUN_TEST(test_store_codes);
    RUN_TEST(test_file_roundtrip);
	RUN_TEST(test_invalid_tree_build);
	printf("[SUMMARY] Total tests executed: %d\n", test_counter);
    return UNITY_END();
}
