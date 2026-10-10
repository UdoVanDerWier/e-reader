# Designing a file format

## magic bytes
usually a sequence of 2 to 4 bytes that more or less uniquely identify a binary format.
Attempts must be made to make sure it doesn't occur that it matches other file format
A string of ASCII text character is a bad choice if it could be mixed with other documents

It is most usefull on systems taht dont have string typing such as a UNIX filesystem.

## header checksum
This could be anything from a single-byte checksum to a 32-bit CRC (Cyclic redundancy check)
to a 128 bit md5 hash. The checksum immediatly follows the magic number and is applied to everything that follows the check sum
and existst before the start of data. Storage is not as stable as you think (i guess writing it over a network is aswell)

## Version number
A necessary field. Applications and file formats evolve overtime and its important to be able to determine wheter the contents of a file are readable or not
There are two basic approaches : serial and major / minor

The serial approach uses a single value often stored in one byte. The number starts at 0..1..2 so on. The application recognizes the versions and support previouse version. And rejects future versions (because they don't exist yet). 

The major/minor approach uses two values. The major version works like the serial version. anything older can usually be handled, anyting newer is rejected
The minor version starts at 0 for each major verison, and goes up when new fields are added. older applications can read newer files because the application knows that when the minor version updates all the previouse fields still exists

### little advice on version numbers
in the prototyping phase i think it would make sense to keep the versions serial. When the design has been proven to work reliably we can start with major minor
Before we go onto the next challenge in this project we first want proof this file type can work.

## offset to data
And older application can read newer data files so long as it knows how to find the fields it cares about and skip the ones it doesn't. The offset to data tells the application how to skip the unrecognized header fields

The offset should always be measured from the start of the file. This makes it easier to do arithmatic on a real file (using SEEK_SET with f_seek) or a memory buffer
Don't use this as a version number seeing it could be easy to just compare the size of the headers of different functions. It mean the file alwys has to grow and we can't remove older fields anymore 

## other fields
Some formats have complex structures. They might have multiple data fields each of which deserves an offest, or have linked lists of objects (e.g. book pages).
One field to seriously consider is a length field. For a file on disk the length of the data is implied by the length of the file. However having an embedded length will let you detect if the file was inadvertenly truncateda, and is very important if your data is ever stream over a network


## struct slurping

It is tempting to read and write files directly from C structs. This is usually done in the name of efficiency or code minimization
Resist this temptation. Historically this has been a horrible idea because structure padding and organisation can vary across platforms, compilers, and even different versions of the one compiler. Explicit pragmas, but your best bet for compatibility is to write fields individually.

Use the standard libc buffered I/O functions (fopen, fread, fwrite, getc, putc). It may "feel" slow to call getc or putc on every byte, but remember that these are fairly small macros that operate on a buffer of data. 

Don't forget to check feof() and ferror() (or equivalents) after doing a series of getc() or putc() calls

## little-endian or big-endian
The best piece of advice here is to use the format that matches up with the most likely consumer of data.  If you're writing a file that will be used predominantly on 80x86 machines, use little-endian ordering for all values.  When reading data

## Checksums on filedata
Putting a CRC on the file data is valuable for the same reasons as putting it on the file header.  The best place for a CRC is actually at the end of a chunk of data.  This allows you to write the data in a stream, without having to seek back to write the CRC.  Very important when streaming data over a network.

A similar argument was made for checksums in file headers, but file headers are (usually) much smaller than the data contained in the file.

## Sources
[fadden.com : file-formats](https://fadden.com/tech/file-formats.html)
