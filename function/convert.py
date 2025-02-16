import os
import tempfile
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def convert_image(file_path, temp_dir, compression_ratio):
    """
    Convert a single image to WebP format with the specified compression ratio.
    """
    image = Image.open(file_path)

    # Resize image if it exceeds WebP limits
    max_size = 16383
    if image.width > max_size or image.height > max_size:
        new_size = (min(image.width, max_size), min(image.height, max_size))
        image.thumbnail(new_size, Image.ANTIALIAS)

    webp_filename = os.path.splitext(os.path.basename(file_path))[0] + '.webp'
    webp_path = os.path.join(temp_dir, webp_filename)
    image.save(webp_path, 'webp', quality=compression_ratio)

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

    # List of image files to be converted
    image_files = [os.path.join(input_dir, filename) for filename in os.listdir(input_dir)
                   if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

    # Use ThreadPoolExecutor to convert images in parallel
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(convert_image, file_path, temp_dir, compression_ratio) for file_path in image_files]

        # Use tqdm to display a progress bar
        for future in tqdm(futures, desc="Converting images", unit="image"):
            future.result()

    return temp_dir

# Example usage:
# temp_dir = convert_images_to_webp('path/to/your/images', 80)
# print(f"Images saved to: {temp_dir}")