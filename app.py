#IMPORTING
import aminofix
from time import sleep
from flask import Flask, jsonify, request

#INIT
app = Flask(__name__)

#API ROUTES
@app.route('/')
def ghoul():
    return jsonify({"answer":None})
@app.route('/ping')
def pingpong():
    return jsonify({"answer": "pong"})
@app.route('/getsid')
def sidextractor():
    emaill = request.args.get('email')
    passwd = request.args.get('passwd')
    proxy = request.args.get('proxy')
        
    if emaill == '' or passwd == '':
        return jsonify({"answer":{"error":{"error_code":1,"error_desc":"No data provided, waited for email and passwd"}}})
    
    try:
        client = aminofix.Client()
        client.login(email=emaill, password=passwd)
        sid = client.sid
        sleep(2)
        client.logout()
        
        return jsonify({"answer":{"sid":sid}})
    except Exception as e:
        exjson = e.args[0]
        try:
            statuscode = exjson['api:statuscode']
            statusinfo = exjson['api:message']
        except:
            statuscode = 2
            statuscode = f"{type(e)}: {e}"

        if statuscode in {200, 213, 214}:
            statusinfo = "Wrong password or/and email. Try again..?"
        elif statuscode in {100, 103, 104, 105, 218}:
            statusinfo = "Seems like Team Amino something did with API again. Check if library works at all. Also you can rewrite API on another lib for Amino, if you want."
        elif statuscode == 111:
            statusinfo = "Sounds like TA doing something with servers. Just wait, i guess."
        elif statuscode in {110, 219, 403}:
            statusinfo = "Summary to host was sent a lot of requests. Just wait a little bit."
        elif statuscode in {210, 246, 293}:
            statusinfo = "Can't log in to the account. It can be deleted or banned by TA, f.e."
        elif statuscode == 270:
            statusinfo = "Your try to get sid here is new, so you should to verify login. Next times when you will try to get sid after verify this problem will disappear, if server will keep IP what it has right now of course."
            return jsonify({"answer":{"error":{"error_code":statuscode,"error_desc":statusinfo, "verifyLink":exjson['url']}}})
        return jsonify({"answer":{"error":{"error_code":statuscode,"error_desc":statusinfo}}})

#START
if __name__ == '__main__':
    # standart run with flask:
    # app.run()
    # running with waitress (much easier because it starts as usual file)
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)