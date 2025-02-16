import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from dotenv import load_dotenv
import pyperclip
from function.convert import convert_images_to_webp
from function.rename import rename_images
from function.upload import upload_to_azure_blob
from database.insert import insert_container, insert_chapter
from database.select import select_containers
from database.index import initialize_database

# Load environment variables from .env file
load_dotenv()

# initialize database
initialize_database()

def extract_chapter_number(folder_name):
    """
    Extract the chapter number from the folder name using a regular expression.
    """
    match = re.search(r'\d+', folder_name)
    if match:
        return int(match.group())
    else:
        raise ValueError("No chapter number found in the folder name.")

def process_chapter(folder_selected, container_name, compression_ratio):
    """
    Process a single chapter: convert images, rename them, and upload to Azure Blob Storage.
    """
    try:
        chapter = extract_chapter_number(os.path.basename(folder_selected))
    except ValueError as e:
        print(e)
        chapter = int(input("Enter the chapter number: "))

    # Convert images to WebP format
    temp_dir = convert_images_to_webp(folder_selected, compression_ratio)
    
    # Rename the converted images
    rename_images(temp_dir, chapter)

    # Upload images to Azure Blob Storage
    image_names = []
    for filename in os.listdir(temp_dir):
        if filename.lower().endswith('.webp'):
            blob_name = f"{filename}"
            file_path = os.path.join(temp_dir, filename)
            upload_to_azure_blob(container_name, blob_name, file_path)
            image_names.append(blob_name)

    # Insert into SQLite database
    insert_chapter(container_name, chapter, image_names)

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)
    print(f"Chapter {chapter} processed successfully.")

def select_multiple_folders():
    """
    Custom dialog to select multiple folders.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folders = []
    while True:
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            folders.append(folder_selected)
            add_more = messagebox.askyesno("Continue", "Do you want to add another folder?")
            if not add_more:
                break
        else:
            break
    return folders

def select_folder_and_convert():
    root = tk.Tk()
    root.withdraw()
    
    # Key-value pair for containers name
    container = select_containers()

    # Prompt if multiple or single chapter
    print("===== Single or Multiple Chapter? =====")
    print("1. Single")
    print("2. Multiple")
    chapter_type = int(input("Enter the desired type: ")) - 1

    # Prompt for title
    print('\n')
    print("===== Select Title =====")
    print("1. Artificial Temperature")
    print("2. Gunbured x Sisters")
    print("3. JK Haru")
    print("4. Mahou Shoujo ni Akogarete")
    print("5. Teisou Gyakuten")
    print("6. Tatoe Hai ni Nattemo")
    print("7. My Food Looks Very Cute")
    print("8. Assassin and Cinderella")
    print("========================")
    title = int(input("Enter the title number: ")) - 1
    container_name = container[title]

    # Prompt for folder selection    
    if chapter_type == 0:  # Single chapter
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            compression_ratio = 60 
            process_chapter(folder_selected, container_name, compression_ratio)
        else:
            print("No folder selected.")
    else:  # Multiple chapters
        folders_selected = select_multiple_folders()
        if folders_selected:
            compression_ratio = 60 
            for folder_selected in folders_selected:
                if os.path.isdir(folder_selected):
                    process_chapter(folder_selected, container_name, compression_ratio)
        else:
            print("No folders selected.")

if __name__ == "__main__":
    select_folder_and_convert()