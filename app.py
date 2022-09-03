#IMPORTING
import json
import aminofix
import requests
from flask import Flask, jsonify, request

#INIT
app = Flask(__name__)
returnAnswers = json.loads(open('./utils/returnAnswers.json').read())
exceptionAnswers = json.loads(open('./utils/exceptionAnswers.json').read())
editException = exceptionAnswers['answerExample']['answer']['error']

###########
#API ROUTES
###########
#start point
@app.route('/')
def startPoint():
    return jsonify(returnAnswers['startPoint'])

###########
#ping point (later will return ping too)
@app.route('/ping')
def pingPong():
    return jsonify(returnAnswers['pingPong'])

###########
#sid getter (get+post)
@app.route('/getsid', methods = ['POST', 'GET'])
def sidextractor():
    if request.method == 'POST':
        emaill, passwd, proxy = emaill = request.form.get('email'), request.form.get('passwd'), request.form.get('proxy')
    else:
        emaill, passwd, proxy = request.args.get('email'), request.args.get('passwd'), request.args.get('proxy')
    proxies = {}
    if proxy:
        proxies = {"https": proxy}

    if emaill == '':
        editException["error_code"], editException["error_desc"] = 1, exceptionAnswers['noEmail']
        return jsonify(exceptionAnswers['answerExample'])
    if passwd == '':
        editException["error_code"], editException["error_desc"] = 1, exceptionAnswers['noPasswd']
        return jsonify(exceptionAnswers['answerExample'])
        
    try:
        client = aminofix.Client(proxies=proxies)
        client.login(email=emaill, password=passwd)
        returnAnswers['returnSid']['answer']['sid'] = client.sid
        client.logout()
        return jsonify(returnAnswers['returnSid'])
    except aminofix.lib.util.exceptions.IpTemporaryBan:
        editException["error_code"], editException["error_desc"] = 403, exceptionAnswers['IPban']
        return jsonify(exceptionAnswers['answerExample'])
    except requests.exceptions.ConnectionError as e:
        if proxy:
            editException['error_desc'] = f"Proxy aborted connection. Try another one. Details: {e}"
        else:
            editException['error_desc'] = f"Connection failed. Try another one. Details: {e}"
        editException['error_code'] = 3
        return jsonify(exceptionAnswers['answerExample'])
    
    except Exception as e:
        exjson = e.args[0]
        try:
            statuscode = editException["error_code"] = exjson['api:statuscode']
        except:
            editException["error_code"], editException["error_desc"] = 2, f"{type(e)}: {e}"
            return jsonify(exceptionAnswers['answerExample'])

        if statuscode in {200, 213, 214}:
            editException["error_desc"] = exceptionAnswers['wrongData']
        elif statuscode in {100, 103, 104, 105, 218}:
            editException["error_desc"] = exceptionAnswers['TAdidShit']
        elif statuscode == 111:
            editException["error_desc"] = exceptionAnswers['maybeMaintenance']
        elif statuscode in {110, 219, 403}:
            editException["error_desc"] = exceptionAnswers["tooManyRequests"]
        elif statuscode in {210, 246, 293}:
            editException["error_desc"] = exceptionAnswers['deletedOrBanned']
        elif statuscode == 270:
            editException["error_desc"] = exceptionAnswers['newLogin']
            editException["verifyLink"] = exjson['url']
        else:
            editException["error_desc"] = exjson['api:message']
        return jsonify(exceptionAnswers['answerExample'])

###########
# S T A R T
###########
if __name__ == '__main__':
    # standart run with flask:
    # app.run()
    # running with waitress (much easier because it starts as usual file)
    from waitress import serve
    serve(app, host="0.0.0.0", port=443)