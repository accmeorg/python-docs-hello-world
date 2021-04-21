from flask import Flask, request, make_response, jsonify
import json
import redis

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
   return "Hello World JSON posted"

@app.route("/redistest", methods=['GET', 'POST'])
def redistest():
    myHostname = "poc-a2subcache.redis.cache.windows.net"
    myPassword = "NJmqGdGgab4ZVlMcGKPbdF48D9JJilL+tExVYI+PU9Y="

    r = redis.StrictRedis(host=myHostname, port=6380,
                          password=myPassword, ssl=True)

    result = r.ping()
    print("Ping returned : " + str(result))

    result = r.set("Message", "Hello!, The cache is working with Python!")
    print("SET Message returned : " + str(result))

    result = r.get("Message")
    print("GET Message returned : " + result.decode("utf-8"))

    result = r.client_list()
    print("CLIENT LIST returned : ")
    for c in result:
        print("id : " + c['id'] + ", addr : " + c['addr'])

    return json.dumps(result)
