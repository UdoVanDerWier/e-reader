## e-reader software MVP Requirements 

### [[Fileformat]] 
- Store a book in a small binary format so it doesn't take up much space on the sdcard
- The file format should support Major/minor version numbers so that when something changes. the older version are still supported. In the major version blocks of the format can be removed. 
- Book data should be stored in the file header 
	- Page numbers, Title, Author, Uitgever, BSN  
- The header should have a file length attribute, Header checksum, Offset to data.
- The pages should be devided in chunks. The chunks
	- it should have a Length attribute, Chunk type attribute (e.g. page, frontpage. backpage.), Page attribute, CRC (Cyclic redudancy check).
	
- The file format must have a magic number.
- For o(1) page search a chunk table would be great. page number with the offset to that page.

### Reading engine
- Stream pages into memory, to keep the e-reader fast we want to have the previouse, current and next page into memory.
- The reading engine should save the state of eachbook  in a file which is loaded into ram on boot. It should also support writes when pages are flipped. When having the page on the sd card it has cross device compatibility. To minimize data corruption and write tear on an sd card it should support a "change" bit and when that bit is set it should write every minute or so. 
### Library and home screen
On the home page show the book title and its author. It would be nice if we could also see the progress. The book should be selected and be able to be opened.

### hardware inputs and navigation
- [ ] navigation buttons
- [ ] select button
- [ ] sd-card
- [ ] battery

### Later.
### Device settings
- [ ] show battery status
- [ ] show and update screen brightness
- [ ] go into sleep mode
- [ ] set wifi (maybe over little webserver)

### file server
- [ ] save file on disk
- [ ] return files that are on disk
