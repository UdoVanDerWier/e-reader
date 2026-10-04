#include <stdint.h>
#include <stdio.h>

// keep Bookheader aligned with the power of 2 and not bigger then 512 bytes so
// that it stays in one sector
struct BookHeader {
  uint8_t MagicByte;
  uint8_t version;

  char title[64];
  char author[64];
  char series[64];

  uint16_t pages;
  uint16_t progress;

  uint16_t page_width;
  uint16_t page_heigth;
  uint8_t bits_per_pixel; // one for black and white. 4 for grayscale

  uint8_t reserved[246]; // keep the rest reserved for later ideas
};

// arguments to give input for book to save
int main(int argc, char *argv[]) { printf("Hello world\n"); }
