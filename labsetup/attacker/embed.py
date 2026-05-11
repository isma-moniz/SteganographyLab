from PIL import Image
import sys
import struct

def embed_payload(input_image, payload_file, output_image):

    # Open image and convert its data into an array of RGB values
    img = Image.open(input_image).convert("RGB")
    pixels = list(img.get_flattened_data())

    new_pixels = []

    for pixel in pixels:
        r,g,b = pixel

        channels = [r,g,b]

        for i in range(3):
            # Toggle off LSB
            channels[i] = channels[i] & 0xFE

        new_pixels.append(tuple(channels))

    out = Image.new(img.mode, img.size)
    out.putdata(new_pixels)
    out.save(output_image)

    print(f"Stego image written to: {output_image}")

if __name__ == "__main__":
    if len (sys.argv) != 4:
        print(
            f"Usage: {sys.argv[0]} <input.png> <payload> <output.png>"
        )
        sys.exit(1)

    embed_payload(
            sys.argv[1],
            sys.argv[2],
            sys.argv[3]
            )
