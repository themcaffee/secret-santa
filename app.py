import os
import uuid
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from pynamodb.models import Model
from pynamodb.attributes import ListAttribute, MapAttribute, UnicodeAttribute
import boto3
from botocore.exceptions import ClientError
import random


FULL_URL = "https://santa." + os.environ["DOMAIN_NAME"]
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": FULL_URL}})


class ParticipantMap(MapAttribute):
  """
  A Participant of a Santa List (ListModel)
  """
  name = UnicodeAttribute()
  email = UnicodeAttribute()
  exclude = UnicodeAttribute()
  ideas = UnicodeAttribute()


class ListModel(Model):
    """
    A DynamoDB Santa List
    """
    class Meta:
        table_name = "santa-list-table-prod"
    uuid = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    password = UnicodeAttribute()
    participants = ListAttribute(of=ParticipantMap)

    def to_dict(self):
        ret_dict = {}
        for name, attr in self.attribute_values.items():
          if name != 'password':
            ret_dict[name] = self._attr2obj(attr)
        
        return ret_dict

    def _attr2obj(self, attr):
        # compare with list class. It is not ListAttribute.
        if isinstance(attr, list):
            _list = []
            for l in attr:
                _list.append(self._attr2obj(l))
            return _list
        elif isinstance(attr, MapAttribute):
            _dict = {}
            for k, v in attr.attribute_values.items():
                _dict[k] = self._attr2obj(v)
            return _dict
        elif isinstance(attr, datetime):
            return attr.isoformat()
        else:
            return attr


class Node:
   def __init__(self, dataval=None):
      self.dataval = dataval
      self.nextval = None


class SLinkedList:
   def __init__(self):
      self.headval = None


"""
Basic route to make sure the service is still alive
"""
@app.route("/")
def hello():
    return "Hello World!"


"""
Create a new santa list in dynamodb
"""
@app.route("/list", methods=['POST'])
def create_list():
  request_data = request.get_json()
  santa_list = ListModel(uuid=str(uuid.uuid4()), name=request_data['name'], password=request_data['password'], participants=[])
  santa_list.save()
  data = {'success': True, 'list': {'uuid': santa_list.uuid, 'name': santa_list.name}}
  return jsonify(data)


"""
Get an existing santa list from dynamodb
"""
@app.route("/list/<id>", methods=['GET'])
def get_list(id):
  try:
    santa_list = ListModel.get(str(id))
    return jsonify({"success": True, "list": santa_list.to_dict()})
  except ListModel.DoesNotExist:
    return jsonify({'success': False}), 404


"""
Add a new participant to an existing santa list. Returns 404 if the list isn't found.
"""
@app.route("/list/<id>/participant", methods=["POST"])
def create_participant(id):
  request_data = request.get_json()
  try:
    santa_list = ListModel.get(str(id))
    participant = ParticipantMap(name=request_data['name'], email=request_data['email'], exclude=request_data['exclude'], ideas=request_data['ideas'])
    santa_list.update(
        actions=[
        ListModel.participants.set((ListModel.participants|[]).append([participant]))
    ])
    return jsonify({"success": True, "list": santa_list.to_dict()})
  except ListModel.DoesNotExist:
    return jsonify({'success': False}), 404


def send_email(recipient, gift_participant, list_id):
  # The subject line for the email.
  subject = "Your Secret Santa has been selected!"
  # The email body for recipients with non-HTML email clients.
  body_text = ("Secret Santa\r\n"
              "You have been selected to be Secret Santa for {}!\r\n{}/list/{}\r\n%unsubscribe_url%".format(gift_participant.name, FULL_DOMAIN, list_id))
  # The HTML body of the email.
  body_html = """<html>
  <head></head>
  <body>
    <h1>Secret Santa</h1>
    <p>You have been selected to be Secret Santa for {}!</p>
    <a href="{}/list/{}">Gift List</a>
    <br>
    %unsubscribe_url%
  </body>
  </html>
              """.format(gift_participant.name, FULL_DOMAIN, list_id)            
  res = requests.post(
    os.environ['MAILGUN_URL'],
    auth=("api", os.environ['MAILGUN_API_KEY']),
    data={"from": "Santa <santa@" + os.environ["DOMAIN_NAME"] + ">",
      "to": [recipient],
      "subject": "Your Secret Santa Recipient Is Here!",
      "text": body_text,
      "html": body_html})
  print("Mailgun status code:" + str(res.status_code))
  print("Mailgun response:" + str(res.text))
  return True


"""
Match participants and send out emails
"""
@app.route("/list/<id>/send", methods=["POST"])
def send_emails_endpoint(id):
  request_data = request.get_json()
  try:
    santa_list = ListModel.get(str(id))
    if santa_list.password != request_data['password']:
      return jsonify({"success": False}), 403
    random.shuffle(santa_list.participants)
    # Create a linked list of participants
    linked_list = SLinkedList()
    linked_list.headval = Node(santa_list.participants[0])
    last = linked_list.headval
    while len(santa_list.participants) != 0:
      participant = santa_list.participants.pop(0)
      # Skip if names match an exclusion in either direction
      if last.dataval.exclude == participant.name or participant.exclude == last.dataval.name:
        santa_list.participants.append(participant)
        continue
      node = Node(participant)
      last.nextval = node
      last = node
    # Traverse list and print out
    current = linked_list.headval 
    while True:
      print("Name: " + current.dataval.name + "\tMatch: " + current.nextval.dataval.name + "\tExclude: " + current.dataval.exclude)
      if not current.nextval:
        print("Last")
        print("Name: " + current.dataval.name + "\tMatch: " + linked_list.headval.dataval.name + "\tExclude: " + current.dataval.exclude)
        break
      current = current.nextval
    # Send out a test email 
    if not send_email("mitch.mcaffee@gmail.com", linked_list.headval.dataval, id):
      return jsonify({"success": False}), 500
    return jsonify({"success": True})
  except ListModel.DoesNotExist:
    return jsonify({"success": False}), 404
