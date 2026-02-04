from flask import Flask
from flask import request, jsonify
import os
import json

app = Flask(__name__)

user_file = "users.json"

def load_user():
    if not os.path.exists(user_file):
        return []
    with open(user_file,"r") as f:
        return json.load(f)

def save_user(user):
    with open(user_file, "w") as f:
        json.dump(user,f)

@app.route("/")
def health():
    return "backen running"

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    password = data.get("password")

    if not password and not name:
        return jsonify({"error":"why no info ?"}), 400
    
    users = load_user()
    
    for user in users:
        if user["name"] == name:
            return jsonify({"error" : "name already exists"}), 400

    new_user = {
        "name" : name,
        "password" : password
    }

    users.append(new_user)
    save_user(users)
    return jsonify({"message": "success"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data.get("name")
    password = data.get("password")

    if not password and not name:
        return jsonify({"error":"blank entries are not allowed"}), 400
    
    users = load_user()

    for user in users:
        if user["name"] == name and user["password"] == password:
            return jsonify({"message":"success"}), 200
        
    return jsonify({"error":"password or name mismatch"}), 400


if __name__ == "__main__":
    app.run(debug=True)