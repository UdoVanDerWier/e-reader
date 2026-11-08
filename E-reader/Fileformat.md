
Laat het bestand in met memory mapped file Dan kan je werken met pointers ipv open read en seek.

Geen struct slurping. Dit kan zelfs per compiler versie verschillen. ookal kan je door middel van pragma dit al groten deels voorkomen wordt het nog steed niet aangeraden.
# Header

| Fieldname      | Size     | Description                                                                                                                                                                                                     |
| -------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MagicByte      | 4 bytes  | To identify the file                                                                                                                                                                                            |
| HeaderCheckSum | 4 bytes  | CRC TO check the integrity of the file. And at a high level of certainty that it reads what is written. (You can compute the CRC as you write the header bytes out, and don't have to seek back to fill it in.) |
| Major version  | 4 bytes  | The major field goes up when a Major file redesign is needed.                                                                                                                                                   |
| Minor version  | 4 bytes  | The minor version starts at 0 on every new Major version. It goes up when new fields are added. Older fields are left untouched                                                                                 |
| offset to data | 4 bytes  | (from byte 0) This is for backwards compatibity an older version of the code can still parse the data when it knows the offset of the data.                                                                     |
| file length    | 4 bytes  | To know if file is truncated somewhere. Handy for when files are streamed over the network.                                                                                                                     |
| Title length   | 2 bytes  | For variable title length                                                                                                                                                                                       |
| Title          | variable | Title of the book                                                                                                                                                                                               |
| Author length  | 2 bytes  | For variable length of the author                                                                                                                                                                               |
| Author         | variable | Author(s) of the book                                                                                                                                                                                           |
| Chunk count    | 4 bytes  | Amount of chunks                                                                                                                                                                                                |

# Chunk table
Each page is a chunk

| Fieldname  | size | Description                         |
| ---------- | ---- | ----------------------------------- |
| pagenumber | 4    | The page number of chunk            |
| ChunkType  | 1    | Check what type of chunk it is      |
| offset     | 4    | offset (from byte 0)to chunk number |
| length     | 4    | length of the data                  |

# Chunk

| Fieldname      | size     | Description                     |
| -------------- | -------- | ------------------------------- |
| Chunktyp       | 1 byte   | Check what type of chunk it is. |
| offset to data | 4 bytes  | For backwards compatiblity      |
| Pagenumber     | 4 bytes  | The page number                 |
| Length         | 4 bytes  | Length of data                  |
| Data           | variable | Data of the page.               |


[Fadden.com](https://www.fadden.com/tech/file-formats.html)
[CRC vs Checksum](https://www.baeldung.com/cs/crc-vs-checksum)
[PNG fileformat](https://libpng.org/pub/png/spec/iso/index-object.html#5PNG-file-signature)

