import aminofix
from time import sleep
from flask import Flask, jsonify, request, send_file
app = Flask(__name__)

@app.route('/')
def ghoul():
    return jsonify({"answer":{"error":{"error_code":404,"error_desc":"Start location"}}})
@app.route('/ping')
def pingpong():
    return jsonify({"answer": {"ping":"pong"}})
@app.route('/getsid')
def sidextractor():
    emaill = request.args.get('email')
    passwd = request.args.get('passwd')
        
    if emaill == '' or passwd == '' or emaill == None or passwd == None:
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
        except:
            return jsonify({"answer":{"error":{"error_code":2,"error_desc":f"{type(e)}: {e}"}}})
        if statuscode == 200:
            return jsonify({"answer":{"error":{"error_code":statuscode,"error_desc":"Wrong password or email. Try again..?"}}})
        elif statuscode == 270:
            return jsonify({"answer":{"error":{"error_code":statuscode,"error_desc":"Your try to get sid here is new, so you should to verify login. Next times when you will try to get sid after verify this problem will disappear, if server will keep IP what it has right now of course.", "verifyLink":exjson['url']}}})
        elif statuscode == 219:
            return jsonify({"answer":{"error":{"error_code":statuscode,"error_desc":"Summary to host was sent a lot of requests. Just wait a little bit."}}})
        else:
            return jsonify({"answer":{"error":{"error_code":statuscode,"error_desc":exjson['api:message']}}})
        
if __name__ == '__main__':
    app.run()
