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


@app.route("/list", methods=['GET'])
def get_list():
  return jsonify({"name": "test secret list", "participants": [{"name": "mitch", "ideas": "blah blah\nblah blah 2"}]})
