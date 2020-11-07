import sqlite3
import os

class Database():

  def __init__(self):
    # self.conn = sqlite3.connect(':memory:')
    self.conn = sqlite3.connect('./database.db')

    self.cursor = self.conn.cursor()
#    self.cursor.execute("""
#       CREATE TABLE material (
#           name text UNIQUE,
#           description TEXT
#       )""")

#    self.cursor.execute("""
#       CREATE TABLE post (
#           title TEXT UNIQUE,
#           material_id INTEGER,
#           description TEXT
#       )""")

  def add_post(self, post):
    with self.conn:
      self.cursor.execute("insert into post values (?, ?, ?)",
        (post['title'].lower(),
        post['material_id'],
        post['description'].lower()))

    res = self.get_post_by(title=post['title'].lower())[0]
    os.mkdir("/home/Msaeb/mysite/tadweer-flask/static/post/" + str(res['id']))

  def add_material(self, material):
    # print (f"========={str(material)}=====")
    with self.conn:
      self.cursor.execute("insert into material values (? , ?)",
        (material['name'].lower(),
        material.get('description','emepty').lower()))

    res = self.get_material_by(name=material['name'])[0]
    os.mkdir("/home/Msaeb/mysite/tadweer-flask/static/material/" + str(res['id']))

  def get_material_by(self, all_records=False, name=False, id=False):

    if name:
      self.cursor.execute("SELECT rowid, * FROM material WHERE name=?", (name.lower(),) )
    elif id:
      self.cursor.execute("SELECT rowid, * FROM material WHERE rowid=?", (id,) )
    elif all_records:
      self.cursor.execute("SELECT rowid, * FROM material")
    else:
      raise UserWarning("Please atleast one condition")

    res = map(lambda a: {
        'id': a[0],
        'name': a[1],
        'description': a[2],
        'path': '/home/Msaeb/mysite/tadweer-flask/static/material/' + str(a[0])
        },
      self.cursor.fetchall())

    return list(res)

  def get_post_by(self, all_records=False, title=False, id=False):

    if title:
      self.cursor.execute("SELECT rowid, * FROM post WHERE title=?", (title.lower(),))
    elif id:
      self.cursor.execute("SELECT rowid, * FROM post WHERE rowid=?", (id,))
    elif all_records:
      self.cursor.execute("SELECT rowid, * FROM post")
    else:
      raise UserWarning("Please atleast one condition")

    res = map(lambda a: {
        'id': a[0],
        'title': a[1],
        'material_id': a[2],
        'description': a[3],
        'path': '/home/Msaeb/mysite/tadweer-flask/static/post/' + str(a[0]),
        },
      self.cursor.fetchall())

    return list(res)

  def get_material_posts(self, material_id):
    self.cursor.execute("SELECT rowid, * FROM post WHERE material_id=?", (material_id,))

    res = map(lambda a: {
        'id': a[0],
        'name': a[1],
        'material_id': a[2],
        'description': a[3],
        'path': '/home/Msaeb/mysite/tadweer-flask/static/post/' + str(a[0]),
      },
      self.cursor.fetchall())

    return list(res)

  def update_material(self, material_id, name=False, description=False):
    if name:
      with self.conn:
        self.cursor.execute("""UPDATE material SET name=? WHERE rowid=?""",
          (name.lower(), material_id))
    if description:
      with self.conn:
        self.cursor.execute("""UPDATE material SET description=? WHERE rowid=?""",
          (description.lower(), material_id))
    return True

  def remove_post(self, title=False, id=False):
    if title:
      with self.conn:
        self.cursor.execute("DELETE FROM post WHERE title=?", (title.lower(),))
      return True
    elif id:
      with self.conn:
        self.cursor.execute("DELETE FROM post WHERE rowid=?", (id,))
      return True
    else:
      raise UserWarning("Please atleast one condition")
      return False

  def remove_material(self, name=False, id=False):
    if name:
      with self.conn:
        self.cursor.execute("DELETE FROM material WHERE name=?", (name.lower(),))
      return True
    elif id:
      with self.conn:
        self.cursor.execute("DELETE FROM material WHERE rowid=?", (id,))
      return True
    else:
      raise UserWarning("Please atleast one condition")
      return False