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