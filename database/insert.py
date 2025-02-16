import sqlite3

def insert_container(container_name):
    """
    Insert a container into the database.

    :param container_name: Name of the container
    """
    conn = sqlite3.connect('archive.db')
    cursor = conn.cursor()

    # Check if the container already exists
    cursor.execute("SELECT id FROM containers WHERE name = ?", (container_name,))
    if cursor.fetchone() is not None:
        raise ValueError(f"Container '{container_name}' already exists in the database.")

    # Insert the container
    cursor.execute("INSERT INTO containers (name) VALUES (?)", (container_name,))

    conn.commit()
    conn.close()

def insert_chapter(container_name, chapter_name, image_names):
    """
    Insert a chapter and its images into the database.

    :param container_name: Name of the container
    :param chapter_name: Name of the chapter
    :param image_names: List of image names
    """
    conn = sqlite3.connect('archive.db')
    cursor = conn.cursor()

    # Get the container ID
    cursor.execute("SELECT id FROM containers WHERE name = ?", (container_name,))
    container_id = cursor.fetchone()
    if container_id is None:
        raise ValueError(f"Container '{container_name}' does not exist in the database.")

    # Insert the chapter
    cursor.execute("INSERT INTO chapters (container_id, name) VALUES (?, ?)", (container_id[0], chapter_name))
    chapter_id = cursor.lastrowid

    # Insert the images
    for image_name in image_names:
        cursor.execute("INSERT INTO images (chapter_id, name) VALUES (?, ?)", (chapter_id, image_name))

    conn.commit()
    conn.close()