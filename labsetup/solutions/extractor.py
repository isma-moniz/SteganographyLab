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

    bits = []

    # extract all LSBs
    for pixel in pixels:
        r, g, b = pixel

        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

    # get payload size
    length_bits = bits[:32]
    length_bytes = bits_to_bytes(length_bits)

    payload_length = struct.unpack(">I", length_bytes)[0]

    print(f"Embedded payload size: {payload_length} bytes")
    
    # get payload itself, according to the size
    payload_bit_count = payload_length * 8

    payload_bits = bits[32:32 + payload_bit_count]

    payload = bits_to_bytes(payload_bits)

    with open(output_file, "wb") as f:
        f.write(payload)

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
