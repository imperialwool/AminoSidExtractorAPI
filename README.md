# Amino SID Extractor API
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/2.1.x/)
[![Python Requirement](https://img.shields.io/badge/python-%3E%3D3.7-informational?style=for-the-badge)](https://www.python.org/downloads/)
[![Last commit](https://img.shields.io/github/last-commit/toxichead/AminoSidExtractorAPI?style=for-the-badge)](https://github.com/toxichead/AminoSidExtractorAPI/commits/main) [![Issues](https://img.shields.io/github/issues/toxichead/AminoSidExtractorAPI?style=for-the-badge)](https://github.com/toxichead/AminoSidExtractorAPI/issues)

Provides you ability to up your own API for getting SID for Amino (aminoapps.com).
Replit-ready!

## Quick start
How to start:
- install Python3 and pip, if you want you can use venv
- install Flask, Amino.Fix and Waitress by command ``pip install amino.fix flask waitress --upgrade``
- clone repository or download file from repo
- move to directory where you cloned repo/saved file

Two ways to start API:
- starting it with Flask (f.e., `flask run -p 7777 -h 0.0.0.0` will run your API on port 7777 and on all IPs what your server/host have)
- starting it as usual Python file (just needed configuration in first time, but it's not so necessary)

Warning:
- API willn't work on most servers 'cause it will bump into 403 Forbidden error
- if you will be using API a lot, can be "Too many requests" error
- host it on own risk, I disclaim all responsibility, also you free to use this even in production bcause it useless thing lmao
- **if you want to use socks proxy, install `PySocks`** (`pip install PySocks`). also keep in mind that **proxy support is freaking unstable**. i'd be grateful if you will help me to improve it and my ~~bad~~ code

## Routes:
- ``/`` is just start dir lol
- ``/ping`` returns pong, if all's ok (in future will return ping to Amino API).
> Example: ``localhost:7777/ping``
- ``/getsid`` needs _email_ and _passwd_ as arguments, else it'll return error with code 1. If host got SID, it return this.
> Example without proxy: ``localhost:7777/getsid?email=iwant@peace-in.world&passwd=glorytoua``


> Example with proxy: ``localhost:7777/getsid?email=coffee@foo.bar&passwd=uaistheworld&proxy=socks5://1.1.1.1:3333``

## Response handling
All answers are JSON for easiest work with API.

Example of answer: ``{"answer":{"sid":"AnsiMSI...XU2Q"}}``

To get any data, you should move into _answer_ **always**.

## Error handling
If you got error, it will keep in _"answer"_ too, but instead _"sid"_ you will see only _"error"_ thing. It contains details, so I recommend to move into _error_ to see, what error you have got. All errors returns _"error_code"_ and _"error_desc"_.
_"Verification Required"_ error also returns extra field _"verifyLink"_. 

Example of error: ``{"answer":{"error":{"error_code":200,"error_desc":"Wrong password or/and email. Try again..?"}}}``

## Example
In console:
```shell
git clone https://github.com/toxichead/AminoSidExtractorAPI.git
cd AminoSidExtractorAPI
python3 app.py
```
In script:
```python
import aminofix
email = "adbots@are.gay"
password = "adbotscreatorswillburninhell"
sid = requests.get(f"https://your-domain-or-ip.here/getsid?email={email}&passwd={password}")
client = aminofix.Client()
client.login_sid(sid)
# ...
```