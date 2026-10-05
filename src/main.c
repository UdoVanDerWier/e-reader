#include <stdint.h>
#include <stdio.h>

// keep Bookheader aligned with the power of 2 and not bigger then 512 bytes so
// that it stays in one sector
// TODO struct padding
typedef struct {
  uint8_t version;
  uint8_t bits_per_pixel; // one for black and white. 4 for grayscale

  uint16_t MagicByte;
  uint16_t pages;
  uint16_t current_page;

  uint16_t page_width;
  uint16_t page_heigth;

  char title[64];
  char author[64];
  char series[64];

  uint8_t reserved[238]; // keep the rest reserved for later ideas
} BookHeaderData;

typedef union {
  BookHeaderData data;
  uint8_t raw[512];
} BookHeader;

// arguments to give input for book to save
int main(int argc, char *argv[]) {
  BookHeader b_header;
  FILE *fp;
  if (argc > 1) {
    fp = fopen(argv[1], "rb");

    if (fp == NULL) {
      printf("Error opening file");
      return 1;
    }
    fread(b_header.raw, sizeof(b_header.raw), 1, fp);
    fclose(fp);
    printf("%u\n", b_header.data.MagicByte);
  }
}
