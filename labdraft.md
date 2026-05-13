# Steganography Lab

## Notes on container usage

This lab can easily be performed on Linux systems without many dependencies. However, we advise (especially for task 2) the usage of our containers. You will find in the lab a `docker-compose.yml` in the labsetup folder. This file, upon executing `docker-compose up -d` (you may have to use sudo), will spin up two containers, an attacker and a victim. 

Each of these is appropriately named for the task 2 instructions, however you can use either of them, or even your own machine, to perform task 1, as they come with the necessary utilities.

You will find that you need to transfer files between your computer and the containers, for image viewing, text editing, or other purposes. For your convenience, we set up a `volumes` folder. This folder is shared between both containers and the host.

You can easily get a shell in any of the containers by using `docker exec -it <container_name> /bin/bash>.

Once you are done with the containers, running `docker-compose down --rmi all` will destroy them and their images.

## Task 1

One of the more common and easier to understand uses of steganography is to hide images within other images.
By closely interacting with a steganographed image and inspecting it you will come to understand its encodings and how its binary contents can be cleverly manipulated to contain more than is visible at first.

### Task 1.1 - Image viewers are not forensic tools

Take a look at the `challenge.jpg` picture, available in the volumes folder, with any image viewer of your choice. You should see an old scientific magazine's drawing of a gnu. This doesn't really tell us anything. Even if there was a binary payload of a virus in here, the image viewer would
not show us that.

A good surface level inspection tool for many sorts of binary media files (images, videos, PDFs, audio,...) is the `exiftool` command line tool.
Using the provided Docker image or your own Linux computer, inspect the image. You can do so with the command `exiftool <file_name>`.

- Describe the output of the `exiftool` command, noting the MIME and file type.

At first glance, the metadata should not reveal obvious abnormalities. We should not however, overly trust tools. This is because such tools (and image viewers as well) usually detect the JPEG encoding in the file and stop parsing once they encounter the JPEG EOI (End of Image) marker (`0xFF 0xD9`). Any data beyond that marker is usually ignored by standard image viewers.

In order to see if there is something hidden in the file, we will need to understand the file encodings and to use lower level tools.

### Task 1.2. - Image file encodings

Image files are simply binary files, with specific encodings that tell programs how to parse and represent them. In the case of JPEG, a quick look at the Wikipedia page https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format will tell you more about the JFIF (JPEG File Interchange Format) in which JPEG conforming files are encoded.

Independently of what encoding the image file has, it will most certainly contain its own convention for a "header", i.e. a set of specific bytes that signify what encoding the image has, as well as possibly other attributes such as width and height. It is also important to signify when the image data is over. In the case of JPEG, a EOI (end-of-image) byte sequence can be found at the end of the image data. Such identifying byte sequences are commonly called magic bytes or file signatures.

- Using a hex inspection tool, such as `hexdump` or `xxd` try to find the byte sequences characteristic of JFIF files in the binary contents. It might be useful to pipe the output of the program to a pager. You can do that by appending ` | less` to the command. Also remember strings or byte sequences may be broken up in your terminal...
- Some hex visualizers also print ASCII strings. Look for the JFIF string in the file.
- Try to find the EOI indicator. Is there any data past it?

### Task 1.3. - Uncovering the second image

If you completed the previous task, you may have noticed there exists data beyond the EOI indicator of the JPEG image. This is a pretty good indication a second image or file has been concatenated into the carrier image. Indeed, the JPEG standard allows for trailing bytes after the EOI indicator, making it a prime target for concatenation steganography. What you have to do now is to identify what kind of file it is and to extract it.

- Look up encoding byte sequences for other common image file formats, i.e. PNG. Try to locate them using the hex tools mentioned.

At this point, you should have enough information to determine whether another file has been embedded in the carrier image. You have two ways to extract it - using sophisticated tooling such as `binwalk`, a program that can identify and optionally extract embedded files and data, or simply using `dd if=<inputfile> of=<outputfile> bs=1 skip=<beginByte>` to copy out the embedded file byte by byte. Whatever your approach is,
- Describe your process and the resulting file.
- Reflect on why this simple file concatenation technique may evade casual inspection.

Note: `binwalk` is a slightly heavier program than your average util, so we decided to not package it with the containers. You can however quickly spin up a containerized `binwalk` with these instructions: https://github.com/ReFirmLabs/binwalk/wiki/Building-A-Binwalk-Docker-Image.
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

In other words, we have a vessel for data in the form of a bit that will essentially barely change the color of the resulting pixel. 3 bits per pixel (1 LSB per channel) are ours to modify as we please. The only restriction is that the number of bits we want to embed must be smaller than the amount of pixels in the image multiplied by 3.

Another thing to keep in consideration is to use a PNG encoded image as a carrier, since it is a lossless format, as opposed to JPEG.

A great library for manipulating image files is the PIL (pillow) python library. You will find in the `labsetup` folder a python program `embed.py` that toggles all LSBs of an image to 0. Run the program with no payload (just input some random gibberish in that field) on the `duck.png` image. Make sure to output it to a .png as well.
- Can you see any difference between the original image and the resulting image? Why?
- Make the necessary additions and modifications to the code in order to embed the payload into it.

If you're having trouble, make sure to:
- Open the payload file in "rb" mode.
- Convert the payload bytes to a list of bits.
- Embed each of them sequentially into an open "slot" in the image.

In a real world context, the payload would often be obfuscated in some other manner. It could be encrypted, compressed, or a combination of both. A good extra challenge is to experiment with compressing the payload with gzip before embedding it. You will of course have to decompress it upon recovering it as well, with the extra advantage of it not being so obvious to detect.

### Task 2.2. - Delivering the payload

You should now have an apparently harmless image of a duck with a demonstration payload embedded in its least significant bits (LSBs). In order to simulate a more realistic scenario, the image should be delivered to the victim container through a seemingly benign channel. A common and straightforward way to achieve this is to serve the image over HTTP.

In real-world attacks, adversaries often rely on social engineering to convince users to download malicious media files. In other cases, an already compromised system may retrieve additional payloads from a remote server in order to reduce the likelihood of detection and avoid shipping all malicious functionality at once.

In this task, the attacker container will host the steganographic image, while the victim container will download and process it using a simple extractor program.

Hosting the image is easy enough. Simply move it into a folder of your choosing and start a python HTTP server.

```
mkdir -p website && mv infected.png website/.
python -m http.server 8000
```

In the victim container you will find an ```imv_fake.sh``` script. It mimics the command line utility `imv` for image viewing, but instead downloads the malicious image on the provided link, calls `extractor.py` on it and runs `payload.sh`.

- Make the necessary modifications to `extractor.py`in order to have it extract the hidden payload to the destination bash executable.
- Run `imv_fake.sh` with the remote HTTP link and verify if you managed to execute the malicious payload.
- Can you describe plausible real-world scenarios in which similar extractors could realistically execute automatically?

## Task 3 - Steganalysis

It is often difficult to identify steganographic alterations to files, as they are frequently encrypted or compressed, we must therefore rely on more sophisticated methods of analysis to stand a better chance at detecting malicious changes. The field of steganalysis fills this need.

In this section we will explore some steganalysis techniques that attempt to identify artificial changes to file contents by searching for discrepancies in noise patterns and file format behavior.

### Task 3.1 - Noise-Floor Consistency Analysis

Most input devices produce some degree of background noise that follows patterns characteristic of the device. The addition of steganographically embedded code disturbs these patterns, leading to pseudo-random regions in the code.

Noise-Floor Consistency Analysis is a set of techniques aimed at identifying these disturbances. To use it, we must first obtain the noise map of an image in the following steps. It is recommended you use the cv2 library in python for this exercise.

- Apply the embed.py file obtained in Task 2.1 to an image in order to steganographically hide a payload inside of it.
- Apply a GaussianBlur or MedianBlur to the clean and embeded image in order to obtain a denoised estimate of them.
- Find the absolute difference between the original and denoised images, called the residuals.

By doing this we are effectively making a map of how much each value differs from the ones arround it, aproximating the noise produced in that pixel. The result we obtain differs depending on the denoising method used and while the sugested blurs aren't the most sophisticated, they can get a suficiently good result for this exercise.

We can now start analysing the noise-floor. There are several methods we can use but in this exercise we will focus on the analysis of the variance in the noise values. 

- Find the variance value of the residual in both the clean and embeded image.
- Apply the same process to different images and verify in which ones the variance difference is significative and which external factors could be impacting variance.

Is the variance difference significative? Try applying the same process to different images or using different measurements such as Entropy and Neighboor Correlation.

There are several factors that can influence our measurements like textured regions, natural image variability, payload size, and denoising method. It is therefore best to employ a higher variety of measurements when trying to identify steganographical embeddings such as Entropy or Neighboor Correlation.

### Task 3.2 - Format Analysis

In Task 1 we identified an image hidden after an EOI flag in the original jpeg. In doing so we engaged in one of the several branches of Format Analysis, a set of techniques aimed at identifying steganographical additions to files by analysing their file structure, metadata, encoding rules, etc.

In this section we will focus on Metadata Analysis, which works by extracting the metadata from the possibly compromised file and trying to find discrepancies that sugest the file has been altered.

There are two images in the volumes directory labeled "metadata1.jpg" and "metadata2.jpg". You should create a python script to obtain the following metadata flags from each image using pillow:
 - Software
 - DateTimeOriginal
 - DateTime
 - Make
 - Model
 - Image Dimensions
 - Compression Information

Although not always relevant, present, or indicative of steganographical activity, there are certain ways in which these tags can indicate that the picture has been altered, which should alert you against the possible hidden content:

- Software - Can indicate the usage of editing software in allegedly unaltered images.
- DateTimeOriginal/DateTime - Might directly show the file has been edited if there is a discrepancy between the dates.
- Make/Model - Missing values can indicate synthetic generation, editing or general metadata stripping while impossible combination should also tip the analyst off to suspiious activity.
- Image Dimensions - Unexpected dimensions may indicate manipulation.
- Compression Information - Embeddings often require recompression, which might be shown in this field. Unusually low quality can also be an indication of manipulation.

There are, of course, countless other tags that could help you determine the possible of hidden files, as well as more general signs of editing such as the absence of tags that should have been present.

Finnaly, we ask you to try to determine which, if any, of the images' metadata display signs of steganography embeding, justifying your answer with their tag contents.
