from PIL import Image

def embed_payload(input_image, payload_file, output_image):

    # Open image and convert its data into an array of RGB values
    img = Image.open(input_image).convert("RGB")
    pixels = list(img.getdata())

    bit_index = 0
    new_pixels = []

#TODO::
