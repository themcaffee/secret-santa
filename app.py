import os


from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list", methods=['POST'])
def create_list():
  data = request.get_json()
  print(data)
  return jsonify(data)

@app.route("/list", methods=['GET'])
def get_list():
  return jsonify({"list": [1, 2, 3, 4]})