import sqlite3
import tkinter as tk
from tkinter import messagebox
import pyperclip
from function.generateTag import generate_img_tags

def get_containers():
    """
    Retrieve all container names from the database.
    """
    conn = sqlite3.connect('archive.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM containers')
    containers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return containers

def get_chapters(container_name):
    """
    Retrieve all chapter names for a given container from the database.
    """
    conn = sqlite3.connect('archive.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT chapters.name FROM chapters
        JOIN containers ON chapters.container_id = containers.id
        WHERE containers.name = ?
    ''', (container_name,))
    chapters = [row[0] for row in cursor.fetchall()]
    conn.close()
    return chapters

def get_images(container_name, chapter_name):
    """
    Retrieve all image names for a given container and chapter from the database.
    """
    conn = sqlite3.connect('archive.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT images.name FROM images
        JOIN chapters ON images.chapter_id = chapters.id
        JOIN containers ON chapters.container_id = containers.id
        WHERE containers.name = ? AND chapters.name = ?
    ''', (container_name, chapter_name))
    images = [row[0] for row in cursor.fetchall()]
    conn.close()
    return images

def copy_to_clipboard(text):
    """
    Copy the given text to the clipboard.
    """
    pyperclip.copy(text)
    messagebox.showinfo("Success", "HTML <img> tags copied to clipboard!")

def main():
    root = tk.Tk()
    root.title("Select Container and Chapter")
    root.geometry("400x300")  # Set the initial size of the window

    # Container selection
    tk.Label(root, text="Select Container:").pack()
    container_var = tk.StringVar()
    container_menu = tk.OptionMenu(root, container_var, *get_containers())
    container_menu.pack()

    # Chapter selection
    tk.Label(root, text="Select Chapter:").pack()
    chapter_var = tk.StringVar()
    chapter_menu = tk.OptionMenu(root, chapter_var, "")
    chapter_menu.pack()

    def update_chapters(*args):
        container_name = container_var.get()
        chapters = get_chapters(container_name)
        chapter_menu['menu'].delete(0, 'end')
        for chapter in chapters:
            chapter_menu['menu'].add_command(label=chapter, command=tk._setit(chapter_var, chapter))

    container_var.trace('w', update_chapters)

    def generate_and_copy():
        container_name = container_var.get()
        chapter_name = chapter_var.get()
        if not container_name or not chapter_name:
            messagebox.showerror("Error", "Please select both container and chapter.")
            return
        images = get_images(container_name, chapter_name)
        img_tags = generate_img_tags(container_name, images)
        copy_to_clipboard(img_tags)

    tk.Button(root, text="Generate and Copy", command=generate_and_copy).pack()

    root.mainloop()

if __name__ == "__main__":
    main()