from flask import Flask, request, make_response, jsonify,  render_template
import json
import redis
import uuid
import datetime
import urllib.request
import urllib.response
import urllib.error
import urllib.parse
import base64
import WaApi

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
   return "Hello World JSON posted"

@app.route("/wa-apitest", methods=['GET', 'POST'])
def waapitest():

    accountid = '366231'
    contactid = '59385380'
    api_key = 'kyuyahagbxno1xlmjwueooqoan0nch'

    api = WaApi.WaApiClient("cme4ever", "f9wdkodsv0o2xxxe7k8232v852pvnw")
    api.authenticate_with_contact_credentials("jcole@accme.org", "BFL#FEpZzK")
    #api.authenticate_with_contact_credentials("ADMINISTRATOR_USERNAME", "ADMINISTRATOR_PASSWORD")
    contact = api.execute_request("/v2/accounts/"+ accountid + "/contacts/" + contactid)
    print(contact.FirstName)
    print(contact.LastName)
    print(contact.Email)
    return(contact.FirstName + " " + contact.LastName + " " + contact.Email)


@app.route("/wamember", methods=['GET', 'POST'])
def wamember():
    #set up redis cache access
    myHostname = "poc-a2subcache.redis.cache.windows.net"
    myPassword = "NJmqGdGgab4ZVlMcGKPbdF48D9JJilL+tExVYI+PU9Y="
    r = redis.StrictRedis(host=myHostname, port=6380,
                          password=myPassword, ssl=True,decode_responses=True)

    whkey = uuid.uuid4().int
    content = request.get_json()
    accountid = content['AccountId']
    contactid = content['Parameters']['Contact.Id']
    action = content['Parameters']['Action']


    whmessage = {}
    messagetype = content['MessageType']
    whmessage['messagetype'] = messagetype

    api = WaApi.WaApiClient("cme4ever", "f9wdkodsv0o2xxxe7k8232v852pvnw")
    api.authenticate_with_contact_credentials("jcole@accme.org", "BFL#FEpZzK")
    #api.authenticate_with_contact_credentials("ADMINISTRATOR_USERNAME", "ADMINISTRATOR_PASSWORD")
    contact = api.execute_request("/v2/accounts/"+ str(accountid) + "/contacts/" + str(contactid))

    if (messagetype == 'Membership' or messagetype == 'Contact'):
        whmessage['accountid'] = accountid
        whmessage['contactid'] = contactid
        whmessage['action'] = action
        whmessage['firstname'] = contact.FirstName
        whmessage['lastname'] = contact.LastName
        whmessage['email'] = contact.Email


    jcontent = json.dumps(whmessage)
    #print(whmessage)


    #jcontent = json.dumps(content)
    #print(content)
    result = r.set(whkey,jcontent)
    #print (content['AccountId'])
    #print(content['Parameters']['Contact.Id'])
    #print (content)
    return (whmessage)


@app.route("/a2queue", methods=['GET', 'POST'])
def a2queue():
    myHostname = "poc-a2subcache.redis.cache.windows.net"
    myPassword = "NJmqGdGgab4ZVlMcGKPbdF48D9JJilL+tExVYI+PU9Y="

    r = redis.StrictRedis(host=myHostname, port=6380,
                          password=myPassword, ssl=True, decode_responses=True)

    theq = {}
    mymap = r.keys(pattern='*')
    #print(mymap)
    for key in mymap:
        value = r.get(key)
        #print(value)
        theq[key] = value
        json.dumps(value)
        #print(value)

    #print(theq)


    #for idx in theq:
        #jobj = json.dumps(theq[idx]);
        #print(jobj)
        #print(idx + ":" + jobj['Contact.Id'] + "\r")

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
