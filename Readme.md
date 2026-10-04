# DIY E-reader

This is a project to learn c programming, embedded programming, a little bit of 3d modeling and PCB design

## formats : 
```c
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
```

## e-reader Requirements 

### File system
- [] store books in small format to easily find books and find its metadata.
- [] read book from the small format.
- [] should also easily save the progress of the book somewhere
### Reading engine
- [] display the book from the metadata
- [] save the progress of the book when going to next page
- [] go to next and previous page
### Library and home screen
- [] display book title, author and progress
- [] show book cover if available
- [] select and open book
### Device settings
- [] show battery status
- [] show and update screen brightness
- [] go into sleep mode
- [] set wifi (maybe over little webserver)
### hardware inputs and navigation
- [] navigation buttons
- [] select button
- [] sd-card
- [] battery
### file server
- [] save file on disk
- [] return files that are on disk

## Companion Web app requirements
### Content ingestion
