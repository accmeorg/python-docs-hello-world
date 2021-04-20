from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    print (request.is_json)
    content = request.get_json()
    print (content)
    return (content)
    #return 'Hello WOrld JSON posted'
  
