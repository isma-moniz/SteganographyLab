# Steganography Lab

## Task 1

One of the more common and easier to understand uses of steganography is to hide images within other images.
By closely interacting with a steganographed image and inspecting it you will come to understand its encodings and how its binary contents can be cleverly manipulated to contain more than is visible at first.

### Task 1.1 - Image viewers are not forensic tools

Take a look at the `challenge.jpg` picture, with any image viewer of your choice. You should see an old scientific magazine's drawing of a gnu. This doesn't really tell us anything. Even if there was a binary payload of a virus in here, the image viewer would
not show us that.

A good surface level inspection tool for many sorts of binary media files (images, videos, PDFs, audio,...) is the `exiftool` command line tool.
Using the provided Docker image or your own Linux computer, inspect the image. You can do so with the command `exiftool <file_name>`.

- Describe the output of the `exiftool` command, noting the MIME and file type.

At first glance, the metadata should not reveal obvious abnormalities. We should not however, overly trust tools. This is because such tools (and image viewers as well) usually detect the JPEG encoding in the file and stop parsing once they encounter the JPEG EOI (End of Image) marker (`0xFF 0xD9`). Any data beyond that marker is usually ignored by standard image viewers.

In order to see if there is something hidden in the file, we will need to understand the file encodings and to use lower level tools.

### Task 1.2. - Image file encodings

Image files are simply binary files, with specific encodings that tell programs how to parse and represent them. In the case of JPEG, a quick look at the Wikipedia page https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format will tell you more about the JFIF (JPEG File Interchange Format) in which JPEG conforming files are encoded.

Independently of what encoding the image file has, it will most certainly contain its own convention for a "header", i.e. a set of specific bytes that signify what encoding the image has, as well as possibly other attributes such as width and height. It is also important to signify when the image data is over. In the case of JPEG, a EOI (end-of-image) byte sequence can be found at the end of the image data. Such identifying byte sequences are commonly called magic bytes or file signatures.

- Using a hex inspection tool, such as `hexdump` or `xxd` try to find the byte sequences characteristic of JFIF files in the binary contents.
- Some hex visualizers also print ASCII strings. Look for the JFIF string in the file.
- Try to find the EOI indicator. Is there any data past it?

### Task 1.3. - Uncovering the second image

If you completed the previous task, you may have noticed there exists data beyond the EOI indicator of the JPEG image. This is a pretty good indication a second image or file has been concatenated into the carrier image. Indeed, the JPEG standard allows for trailing bytes after the EOI indicator, making it a prime target for concatenation steganography. What you have to do now is to identify what kind of file it is and to extract it.

- Look up encoding byte sequences for other common image file formats, i.e. PNG. Try to locate them using the hex tools mentioned.

At this point, you should have enough information to determine whether another file has been embedded in the carrier image. You have two ways to extract it - using sophisticated tooling such as `binwalk`, a program that can identify and optionally extract embedded files and data, or simply using `dd if=<inputfile> of=<outputfile> bs=1 skip=<beginByte>` to copy out the embedded file byte by byte. Whatever your approach is,
- Describe your process and the resulting file.
- Reflect on why this technique may evade casual inspection.

## Task 2. - Stegomalware

Hiding images inside other images is a very fun and innocent use of steganography. Unfortunately however, such benign use-cases are not always the norm. Hiding malware inside seemingly harmless digital media is a crafty way to avoid traditional signature-based and sandbox-based detection. With stegomalware, the payload remains embedded and obfuscated inside a media file and is extracted at runtime.

Multiple high-profile cyber attacks and campaigns have been documented to make use of stegomalware in one way or another: Cerber (2016) concealed executable Ransomware code in JPEG images, Waterbug (2019) injected malicious DLLs into WAV audio files, among others. There are multiple ways to hide malware inside media, in ways much more sophisticated than simply appending a payload to the end of a file. In this task, you will explore LSB encoding of payloads into image files, as well as craft an extractor tool to retrieve and execute the (harmless) payload.

### Task 2.1. - Embedding the Payload

Inside the Attacker container, you will find a shell script with the following contents:

```payload.sh
#!/bin/bash
echo "[demo] payload execution successful!"
touch /tmp/stego_malware_executed
```

To hide this payload, you will use the least significant bits of the image colors. What does this mean?

In image files, each pixel is the unit of color. They often can be specified using the RGB model, meaning they can be specified as pixel(Red, Green, Blue), where each of the components is a value between 0 and 255. Each pixel takes 3 bytes of memory (assuming they don't have an Alpha channel), which means each component will have 8 bits. Among these bits, the least significant bit will have the least weight on the value of the channel. For example, assuming we have:

	R = 11111111 = 255
	
If we switch "off" the LSB we will have:

	R = 11111110 = 254
	
If we switch "off" the MSB we will have:

	R = 01111111 = 127

In other words, we have a vessel for data in the form of a bit that will essentially barely change the color of the resulting pixel. 3 bits per pixel (1 LSB per channel) are ours to modify as we please. The only restriction is that the number of bits we want to embed must be smaller than the amount of pixels in the image divided by 3.

Another thing to keep in consideration is to use a PNG encoded image as a carrier, since it is a lossless format, as opposed to JPEG.

A great library for manipulating image files is the PIL (pillow) python library. You will find in the `labsetup` folder a python program `embed.py` that toggles all bits of an image to 0. Run the program with on any image of your choosing.
- Can you see any difference? Why?
- Make the necessary additions and modifications to the code in order to embed the payload into it.
- TODO add more