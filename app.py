import os


from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list", methods=['POST'])
def create_list():
  data = {'success': True}
  return jsonify(data)


@app.route("/list/<id>", methods=['GET'])
def get_list(id):
  return jsonify({"name": "test secret list", "participants": [{"name": "mitch", "ideas": "blah blah\nblah blah 2"}]})
