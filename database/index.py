import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect('archive.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table to store container information
cursor.execute('''
CREATE TABLE IF NOT EXISTS containers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)
''')

# Create a table to store chapter information
cursor.execute('''
CREATE TABLE IF NOT EXISTS chapters (
    id INTEGER PRIMARY KEY,
    container_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (container_id) REFERENCES containers(id)
)
''')

# Create a table to store image information
cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY,
    chapter_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id)
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()