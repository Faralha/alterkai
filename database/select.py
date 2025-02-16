import sqlite3

def select_containers():
  """
  Select all containers from the database.

  :return: List of container names
  """
  conn = sqlite3.connect('archive.db')
  cursor = conn.cursor()

  cursor.execute("SELECT name FROM containers")
  containers = [row[0] for row in cursor.fetchall()]

  conn.close()
  return containers

def select_chapter(container_name, chapter):
  """
  Select a chapter from the database.

  :param container_name: Name of the container
  :param chapter: Chapter number
  :return: List of image names
  """
  conn = sqlite3.connect('archive.db')
  cursor = conn.cursor()

  cursor.execute('''
  SELECT images.name
  FROM images
  JOIN chapters ON images.chapter_id = chapters.id
  JOIN containers ON chapters.container_id = containers.id
  WHERE containers.name = ? AND chapters.name = ?
  ''', (container_name, chapter))

  images = [row[0] for row in cursor.fetchall()]

  conn.close()
  return images

def select_all_chapters(container_name):
  """
  Select all chapters from the database.

  :param container_name: Name of the container
  :return: Dictionary of chapter names and image names
  """
  conn = sqlite3.connect('archive.db')
  cursor = conn.cursor()

  cursor.execute('''
  SELECT chapters.name, images.name
  FROM images
  JOIN chapters ON images.chapter_id = chapters.id
  JOIN containers ON chapters.container_id = containers.id
  WHERE containers.name = ?
  ''', (container_name,))

  chapters = {}
  for row in cursor.fetchall():
    chapter_name = row[0]
    image_name = row[1]
    if chapter_name not in chapters:
      chapters[chapter_name] = []
    chapters[chapter_name].append(image_name)

  conn.close()
  return chapters