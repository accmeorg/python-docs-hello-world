from flask import Flask, request, make_response, jsonify
import json

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
   return "Hello World JSON posted"
  
@app.route("/wamember", methods=['GET', 'POST'])
def wamember():
    #print (request.is_json)
    content = request.get_json()
    #print (content)
    return json.dumps(content)
    #return ("Hello World - in wamember")
