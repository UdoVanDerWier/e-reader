from enum import auto
import struct

import pymupdf

MAGIC_BYTE = b"KUDO"
MAJOR = 0
MINOR = 0

doc = pymupdf.open("a.pdf")

offset = 0 # to data. calculate this dynamicly
filelength = 0 # geld het zelfde

title = b"dorenroosje"
author = b"Benthe de Goede"
with open('file2.bin', 'wb') as f : 
    header_format = ">4s III"
    # 4 byte char MAGIC_Byte
    # major version 4 bytes uint
    # minor version 4 bytes uint
    # offset to data 4 bytes uint
    # file length 4 bytes uint
    header = struct.pack(
        header_format,
        MAGIC_BYTE,
        MAJOR,
        MINOR,
        offset,
        filelength
    )

    f.write(header)
    title_length = struct.pack(
        ">H",
        len(title)
    )
    f.write(title_length)
    f.write(title)

    author_length = struct.pack(
        ">H",
        len(author)
    )
    f.write(author)


    # f.write() # minor version 4 bytes uint
    # f.write() # offset to data 4 bytes uint
    # f.write() # file length 4 bytes uint
    # f.write() # title length 2 bytes uint
    # f.write() # title variable
    # f.write() # Author length 2 bytes uint
    # f.write() # Author variable
    # f.write() # Chunk count 4 bytes uint