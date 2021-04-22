from flask import Flask, request, make_response, jsonify,  render_template
import json
import redis

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
   return "Hello World JSON posted"

@app.route("/wamember", methods=['GET', 'POST'])
def wamember():
    #set up redis cache access
    myHostname = "poc-a2subcache.redis.cache.windows.net"
    myPassword = "NJmqGdGgab4ZVlMcGKPbdF48D9JJilL+tExVYI+PU9Y="
    r = redis.StrictRedis(host=myHostname, port=6380,
                          password=myPassword, ssl=True)

    #print (request.is_json)
    content = request.get_json()
    print(content)
    jcontent = json.dumps(content)
    print(jcontent)
    result = r.set(content['AccountId'],jcontent)
    #print (content['AccountId'])
    #print (content)
    return json.dumps(content)
    #return ("Hello World - in wamember")


@app.route("/a2queue", methods=['GET', 'POST'])
def a2queue():
    myHostname = "poc-a2subcache.redis.cache.windows.net"
    myPassword = "NJmqGdGgab4ZVlMcGKPbdF48D9JJilL+tExVYI+PU9Y="

    r = redis.StrictRedis(host=myHostname, port=6380,
                          password=myPassword, ssl=True, decode_responses=True)

    theq = {}
    mymap = r.keys(pattern='*')
    print(mymap)
    for key in mymap:
        value = r.get(key)
        print(value)
        theq[key] = value

    print(theq)


    #for idx in theq:
        #print(idx + ":" + theq[idx]['Parameters']['Contact.Id'] + "\r")

    return render_template('index.html', title='Wild Apricot Users Pending Xfer to ACCME Academy', queue=theq)

    return ("cache dumped")


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

    r.flushdb()
    return json.dumps(result)
