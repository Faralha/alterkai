import os
import tempfile
from PIL import Image

def convert_images_to_webp(input_dir, compression_ratio):
    """
    Convert all images in the input directory to WebP format with the specified compression ratio.
    Output the converted images to a temporary directory.

    :param input_dir: Directory containing images to be converted
    :param compression_ratio: Compression ratio for the WebP format (0 to 100)
    """
    if not os.path.isdir(input_dir):
        raise ValueError(f"The provided path '{input_dir}' is not a directory or does not exist.")

    temp_dir = tempfile.mkdtemp()
    # print(f"Converted images will be saved to temporary directory: {temp_dir}")

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            file_path = os.path.join(input_dir, filename)
            image = Image.open(file_path)
            webp_filename = os.path.splitext(filename)[0] + '.webp'
            webp_path = os.path.join(temp_dir, webp_filename)
            image.save(webp_path, 'webp', quality=compression_ratio)
            print(f"Converted {filename} to {webp_filename} with compression ratio {compression_ratio}")

    return temp_dir

# Example usage:
# temp_dir = convert_images_to_webp('path/to/your/images', 80)
# print(f"Images saved to: {temp_dir}")