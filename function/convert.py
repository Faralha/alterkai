import os
import tempfile
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def convert_image(file_path, temp_dir, compression_ratio):
    """
    Convert a single image to WebP format with the specified compression ratio.
    If the image exceeds WebP limits, cut it into multiple pieces.
    """
    image = Image.open(file_path)

    # Resize image if it exceeds WebP limits
    max_size = 16383
    if image.width > max_size or image.height > max_size:
        pieces = []
        if image.width > max_size:
            # Cut the image into vertical pieces
            num_pieces = (image.width // max_size) + 1
            for i in range(num_pieces):
                left = i * max_size
                right = min((i + 1) * max_size, image.width)
                piece = image.crop((left, 0, right, image.height))
                pieces.append(piece)
        elif image.height > max_size:
            # Cut the image into horizontal pieces
            num_pieces = (image.height // max_size) + 1
            for i in range(num_pieces):
                top = i * max_size
                bottom = min((i + 1) * max_size, image.height)
                piece = image.crop((0, top, image.width, bottom))
                pieces.append(piece)
        else:
            # Cut the image into both vertical and horizontal pieces
            num_pieces_width = (image.width // max_size) + 1
            num_pieces_height = (image.height // max_size) + 1
            for i in range(num_pieces_width):
                for j in range(num_pieces_height):
                    left = i * max_size
                    right = min((i + 1) * max_size, image.width)
                    top = j * max_size
                    bottom = min((j + 1) * max_size, image.height)
                    piece = image.crop((left, top, right, bottom))
                    pieces.append(piece)

        # Save each piece as a separate WebP file
        for index, piece in enumerate(pieces, start=1):
            webp_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}-{index:02d}.webp"
            webp_path = os.path.join(temp_dir, webp_filename)
            piece.save(webp_path, 'webp', quality=compression_ratio)
    else:
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