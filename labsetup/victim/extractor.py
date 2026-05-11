from PIL import Image
import struct
import sys

# the opposite of bytes_to_bits...
def bits_to_bytes(bits):
    output = bytearray()

    for i in range(0, len(bits), 8):
        byte = 0

        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit

        output.append(byte)

    return bytes(output)


def extract_payload(input_image, output_file):
    img = Image.open(input_image).convert("RGB")
    pixels = list(img.get_flattened_data())


# TODO: complete this

    print(f"Extracted payload written to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            f"Usage: {sys.argv[0]} <input.png> <output_payload>"
        )
        sys.exit(1)

    extract_payload(
        sys.argv[1],
        sys.argv[2]
    )
