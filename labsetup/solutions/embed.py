from PIL import Image
import sys
import struct

# Convert bytes into list of bits for ease of access
def bytes_to_bits(data):
    bits = []

    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def embed_payload(input_image, payload_file, output_image):
    if not output_image.lower().endswith(".png"):
        raise ValueError("Output must be a .png file to preserve LSB data.")

    # Open image and convert its data into an array of RGB values
    img = Image.open(input_image).convert("RGB")
    pixels = list(img.get_flattened_data())

    with open(payload_file, "rb") as f:
        payload = f.read()

    payload_length = struct.pack(">I", len(payload))
    full_payload = payload_length + payload
    payload_bits = bytes_to_bits(full_payload)

    capacity = len(pixels) * 3 # RGB bytes we can fit a bit into

    if len(payload_bits) > capacity:
        raise ValueError(
                f"Payload too large.\n"
                f"Need {len(payload_bits)} bits, "
                f"but image only supports {capacity} bits."
                )
    bit_index = 0
    new_pixels = []

    for pixel in pixels:
        r,g,b = pixel

        channels = [r,g,b]

        for i in range(3):
            if bit_index < len(payload_bits):
                # set new bit
                channels[i] = (channels[i] & 0xFE) | payload_bits[bit_index]
                bit_index += 1

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

