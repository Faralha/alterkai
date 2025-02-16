import os
import re
from tqdm import tqdm

def natural_sort_key(s):
    """
    Key function for natural sorting.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def rename_images(temp_dir, chapter):
    """
    Rename images in the temporary directory based on the given chapter number.
    The images will be renamed in the format 'chapter-page.webp'.

    :param temp_dir: Directory containing the images to be renamed
    :param chapter: Chapter number to be used in the new filenames
    """
    if not os.path.isdir(temp_dir):
        raise ValueError(f"The provided path '{temp_dir}' is not a directory or does not exist.")

    images = [f for f in os.listdir(temp_dir) if f.lower().endswith('.webp')]
    images.sort(key=natural_sort_key)  # Ensure the images are sorted naturally

    for index, filename in enumerate(tqdm(images, desc="Renaming images", unit="image"), start=1):
        new_filename = f"{chapter:02d}-{index:02d}.webp"
        old_path = os.path.join(temp_dir, filename)
        new_path = os.path.join(temp_dir, new_filename)
        os.rename(old_path, new_path)

# Example usage:
# temp_dir = '/path/to/temp/dir'
# rename_images(temp_dir, 10)