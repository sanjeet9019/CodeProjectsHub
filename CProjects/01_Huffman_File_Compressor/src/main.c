/******************************************************************************
 *  File         : main.c
 *  Author       : Sanjeet Prasad
 *  Email        : sanjeet8.23@gmail.com
 *  Description  : CLI orchestration for Huffman compression and decompression
 *                 - Accepts input/output filenames via command-line or defaults
 *                 - Invokes compression and decompression routines
 *                 - Reports file sizes and previews byte-level content
 *  Date         : 22-10-2025
 *  Language     : C (GCC)
 ******************************************************************************/

#include "../include/huffman.h"

#define PREVIEW_BYTES 50  // Number of bytes to preview per file

int main(int argc, char* argv[]) {
    const char* input_file;
    const char* compressed_file   = "data/compressed.bin";
    const char* decompressed_file = "data/decompressed.txt";

    // Handle CLI arguments
    if (argc == 2) {
        input_file = argv[1];
        printf("[HUFFMAN]: Using input file: %s\n", input_file);
    } else if (argc == 1) {
        input_file = "data/input.txt";
        log_message("INFO", "No input file provided. Using default:");
        printf("  Input       : %s\n", input_file);
    } else {
        printf("\nUsage:\n");
        printf("  %s <input_file>\n", argv[0]);
        printf("  OR run without arguments to use default file in ./data/\n");
        return 1;
    }

    // Validate input file type
    if (!is_supported_file(input_file)) {
        log_message("ERROR", "Unsupported file type.");
        return 1;
    }

    // Compression
    log_message("INFO", "Starting compression...");
    compress_file(input_file, compressed_file);
    printf("[HUFFMAN]: Compression finished. Encoded output saved to: %s\n", compressed_file);

    // Decompression
    log_message("INFO", "Starting decompression...");
    decompress_file(compressed_file, decompressed_file);
    printf("[HUFFMAN]: Decompression finished. Restored output saved to: %s\n", decompressed_file);

    // File size report
    long input_size       = file_size(input_file);
    long compressed_size  = file_size(compressed_file);
    long decompressed_size= file_size(decompressed_file);

    printf("\n[HUFFMAN]: File Size Report\n");
    printf("  Input File       : %s (%ld bytes)\n", input_file, input_size);
    printf("  Compressed File  : %s (%ld bytes)\n", compressed_file, compressed_size);
    printf("  Decompressed File: %s (%ld bytes)\n", decompressed_file, decompressed_size);

    if (input_size > 0) {
        double ratio = 100.0 * (1.0 - ((double)compressed_size / input_size));
        printf("  Compression Ratio: %.2f%%\n", ratio);
    }

    // Byte previews
    printf("\n[HUFFMAN]: Byte Previews (first %d bytes)\n", PREVIEW_BYTES);

    printf("  Input File       :\n");
    preview_bytes(input_file, PREVIEW_BYTES);

    printf("  Compressed File  :\n");
    preview_bytes(compressed_file, PREVIEW_BYTES);

    printf("  Decompressed File:\n");
    preview_bytes(decompressed_file, PREVIEW_BYTES);

    return 0;
}
