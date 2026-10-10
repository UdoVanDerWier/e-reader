#include <stdint.h>
#include <stdio.h>

const uint16_t MAGIC_BYTE = 69;
// keep Bookheader aligned with the power of 2 and not bigger then 512 bytes so
// that it stays in one sector
typedef struct {
  uint8_t version;
  uint8_t bits_per_pixel; // one for black and white. 4 for grayscale

  uint16_t MagicByte;
  uint16_t pages;
  uint16_t current_page;   // keep in ram when book is open
  uint16_t offset_to_data; // byte_size // dynamic so that we can easily go to
                           // the previouse page
  char title[64];
  char author[64];
  char series[64];

  uint8_t reserved[238]; // keep the rest reserved for later ideas
} BookHeaderData;

typedef union {
  BookHeaderData data;
  uint8_t raw[512];

} BookHeader;

typedef struct {
  uint8_t flags; // e.g. Bookmarks, images, etc.

  uint16_t page_number;
  uint16_t page_width;  // TODO heb ik dit nodig?
  uint16_t page_height; // TODO heb ik dit nodig?

  uint32_t file_offset;
  uint32_t data_size;

} PageData;

int validate_file_type(FILE *fp) {
  if (fseek(fp, 2, SEEK_SET) != 0) {
    printf("Error finding magicbyte\n");
    return 1;
  }
  uint16_t magicbyte = 0;
  fread(&magicbyte, sizeof(magicbyte), 1, fp);
  rewind(fp);

  if (magicbyte != MAGIC_BYTE) {
    printf("Couldn't find magicbyte\n");
    return 1;
  }
  return 0;
}
// arguments to give input for book to save
int main(int argc, char *argv[]) {
  BookHeader b_header;
  FILE *fp;
  if (argc > 1) {
    fp = fopen(argv[1], "rb");

    if (fp == NULL) {
      printf("Error opening file\n");
      return 1;
    }

    if (validate_file_type(fp) != 0) {
      return 1;
    }
    // TODO save file on disk else throw error
    // TODO chunk the pages. Instead of loading the entire book into memory
    fread(b_header.raw, sizeof(b_header.raw), 1, fp);
    fclose(fp);
    // would i make sense to first load the magicbyte to check and then load the
    // whole file into memory
  }
}
