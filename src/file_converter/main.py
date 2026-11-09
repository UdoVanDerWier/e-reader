from enum import Enum
import struct

import pymupdf

MAGIC_BYTE = b"KUDO"
MAJOR = 0
MINOR = 2

HEADER_LENGTH = 32 # this is without the variable title and author length
META_DATA_LENGTH = 24
HEADER_FORMAT = ">4sIIIII"
TABLE_FORMAT = ">IBII"
doc = pymupdf.open()

class PageType(Enum) :
    PAGE = 0 

class DocConvert : 
    def __init__(self, path, output_path) : 
        self.doc = pymupdf.open(path)
        self.output_path = output_path
        self.major = MAJOR
        self.minor = MINOR
        self.magic=  MAGIC_BYTE

        self.file_length = 0
        self.header_length = 0

        self.chunk_table = {}
        self.pages = []

    def convert(self) : 
        self.__get_chunk_data()

        with open(self.output_path, "wb") as f : 
            self.__write_metadata(f)
            self.__write_pages(f)

    def __write_pages(self, file) : 
        if self.header_length > 0 : 
            print("you have not written a header yet")
        file.seek(self.header_length)
        for p in self.pages : 
            file.write(p)

    def __write_chunk_table(self, file, offset) : 
        chunk_table_format = "<IBII"
        file.seek(offset)
        length = 0
        for page in self.chunk_table : 
            table_col = self.chunk_table.get(page)
            file.write(
                struct.pack(
                    chunk_table_format,
                    page,
                    table_col.get("type").value,
                    table_col.get("offset"),
                    table_col.get("length")
                )
            )
            length += 13

        return length

    def __write_metadata(self, file) :
        header_format = "<4sIIIII"

        book_data_len = self.__write_book_data(file)
        offset = META_DATA_LENGTH + book_data_len
        chunk_table_length = self.__write_chunk_table(file, offset)
        file.seek(0)
        file.write(
            struct.pack(
                header_format,
                self.magic,
                0,
                self.major,
                self.minor,
                offset,
                self.file_length + offset + chunk_table_length,
            )
        )
        self.header_length = META_DATA_LENGTH + book_data_len + chunk_table_length
        print(f"file length : {self.file_length + offset + chunk_table_length}")



    def __write_book_data(self, file):
        attr_len = 8
        title_len, title = self.__get_title()
        author_len, author = self.__get_author()
        chunk_c = self.__get_chunk_count()

        file.seek(META_DATA_LENGTH)
        self.__write_variable(file, title_len, title)
        self.__write_variable(file, author_len, author)

        file.write(
            struct.pack(
                "<I",
                chunk_c
            )
        )

        return title_len + author_len + attr_len
         

    def __get_title(self) :
        title = self.doc.metadata.get("title")
        length = len(title)

        return length, title.encode("utf-8")
    
    def __get_author(self) :
        author = self.doc.metadata.get("author")
        length = len(author)

        return length, author.encode("utf-8")

    def __get_chunk_count(self) : 
        return self.doc.page_count - 1

    def __get_chunk_data(self) :
        for i, p in enumerate(self.doc.pages(start=1), start=1) :
            text = p.get_text()

            try : 
                t = text.encode('utf-8')
                t_len = len(t)
                self.chunk_table[i] = {
                    "type": PageType.PAGE,
                    "offset": self.file_length,
                    "length": t_len
                }

                self.pages.append(t)
                self.file_length += t_len

                print(f"f_len : {self.file_length} | page {i} | page_len {t_len}")
            except UnicodeError : 
                print("String is not utf-8")

    def __write_variable(self, file, length, text) :
        file.write(
            struct.pack(
                "<H",
                length
            ) 
        )

        file.write(text)

class DocDecode : 
    def __init__(self, path) :
        self.path = path
        self.meta = {}
        self.book_data = {}
        self.table = {}

    def decode(self) :
        with open(self.path, 'rb') as f:
            f.seek(0)
            if f.read(4) != MAGIC_BYTE : 
                print("magic byte invalid")

            self.meta = self.__load_meta_data(f)
            self.table = self.__load_table_data(f, self.meta.get("page_count"), self.meta.get("data_offset"))


    def get_page(self, num) : 
        offset = self.table[num].get("offset")
        length = self.table[num].get("length")

        with open(self.path, 'rb') as f : 
            f.seek(offset)
            print(f.read(length).decode())
    
    def __load_meta_data(self, f) :
        f.seek(META_DATA_LENGTH)
        title_len = self._to_int(f.read(2))
        title = f.read(title_len).decode()
        author_len = self._to_int(f.read(2))
        author = f.read(author_len).decode()
        page_count = self._to_int(f.read(4))

        f.seek(4)
        return {
            "checksum": self._to_int(f.read(4)),
            "major": self._to_int(f.read(4)),
            "minor": self._to_int(f.read(4)), 
            "data_offset": self._to_int(f.read(4)),
            "file_length": self._to_int(f.read(4)),
            "title": title,
            "author": author,
            "page_count": page_count 
        }

    def __load_table_data(self, f, pages_count, offset) :
        f.seek(offset) 
        table = {}
        for _ in range(0, pages_count) :
            num = self._to_int(f.read(4)) 
            table[num] = {
                "type": self._to_int(f.read(1)),
                "offset": self._to_int(f.read(4)),
                "length": self._to_int(f.read(4))
            }

        return table

    def _to_int(self, val) :
        return int.from_bytes(val, byteorder="little", signed=False)

DocConvert("./pg79933-images-3.epub", "./test.bin").convert()
dec = DocDecode("./test.bin")
dec.decode()
dec.get_page(4)
