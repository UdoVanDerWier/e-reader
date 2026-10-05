import struct
import pymupdf

VERSION = 4
# MAGICK_BYTE = "DIYR"
MAGICK_BYTE = 69 

# typedef struct {
#  uint8_t version;
#  uint8_t bits_per_pixel; // one for black and white. 4 for grayscale
#
#  uint16_t MagicByte;
#  uint16_t pages;
#  uint16_t current_page;
#
#  uint16_t page_width;
#  uint16_t page_heigth;
#
#  char title[64];
#  char author[64];
#  char series[64];
#
#  uint8_t reserved[238]; // keep the rest reserved for later ideas
#} BookHeaderData;
HEADER_FORMAT = "@BBHHHHH64s64s64s238s"

file_name = input("file input")
output = input("output file")

doc = pymupdf.open(file_name)
header = struct.pack(HEADER_FORMAT, VERSION, 1, MAGICK_BYTE, 310, 10, 400, 240, "harry potter".encode("utf-8").ljust(64, b'\x00'), "J.K. Rolling".encode("utf-8").ljust(64, b'\x00'), "J.K. Rolling".encode("utf-8").ljust(64, b'\x00'), b'\0x00'*238)

with open(output, "wb") as f : 
    print("opening file, {}".format(f.name))
    f.write(header)
