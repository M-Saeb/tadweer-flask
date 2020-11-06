from flask import Flask, render_template, jsonify, request
import sqlite3
from flask_cors import CORS, cross_origin
from database import Database
from tables import Post, Material 

app = Flask(__name__)
CORS(app)


@app.route('/api/post/add', methods=['POST'])
def add_post():
  if request.method == "POST":
    db = Database()
    data = request.get_json()
    try:
      db.add_post(data)
    except sqlite3.IntegrityError as e:
      return "Post already Exist: " + str(e)
    post_id = db.get_post_by(title=data['title'])
    return str(post_id[0]['id'])

@app.route('/api/material/add', methods=['POST'])
def add_material():
  if request.method == "POST":
    db = Database()
    data = request.get_json()
    try:
      db.add_material(data)
    except sqlite3.IntegrityError as e:
      return "Material already Exist: " + str(e) 
    post_id = db.get_material_by(name=data['name'])
    return str(post_id[0]['id'])

@app.route('/api/material', methods=['GET'])
def get_materials():
  if request.method == "GET":
    material_id = request.args.get("id")
    material_name = request.args.get("name")
    db = Database()
    if material_id:
      res = db.get_material_by(id=material_id)
      return jsonify(res)

    elif material_name:
      res = db.get_material_by(name=material_name)
      return jsonify(res)

    else:
      res = db.get_material_by(True)
      return jsonify(res)

@app.route('/api/post', methods=["GET"])
def get_post():
  if request.method == "GET":
    title = request.args.get("title")
    id = request.args.get("id")
    material_id = request.args.get("material_id")
    db = Database()
    if title:
      res = db.get_post_by(title=titll.replace('_',' '))
      return jsonify(res)

    elif id:
      res = db.get_post_by(id=id)
      return jsonify(res)

    elif material_id:
      res = db.get_material_posts(material_id)
      return jsonify(res)

    else:
      res = db.get_post_by(True)
      return jsonify(res)

@app.route('/api/material/update', methods=['POST'])
def update_material():
  if request.method == "POST":
    db = Database()
    data = request.get_json()
    db.update_material(
      data["id"],
      data.get("name", False),
      data.get("description", False))
    res = db.get_material_by(id=data["id"])
    return jsonify(res[0])

@app.route('/api/post/remove', methods=['POST'])
def remove_post():
  if request.method == "POST":
    db = Database()
    data = request.get_json()
    res = db.remove_post(
      data.get("title", False),
      data.get("id", False))
    return jsonify(res)

@app.route('/api/material/remove', methods=['POST'])
def remove_material():
  if request.method == "POST":
    db = Database()
    data = request.get_json()
    res = db.remove_material(
      data.get("name", False),
      data.get("id", False))
    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True) #localIP:5000, so the api call url should be "192.168.x.x:5000/api"
