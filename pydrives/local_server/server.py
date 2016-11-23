#!/usr/bin/env python3
from flask import request
from flask import Flask
import redis

app = Flask(__name__)


@app.route("/")
def get_auth_key():
    refresh_token = request.args.get('state')
    auth_token = request.args.get('code')
    r.set(refresh_token, auth_token)
    return 'You are authorized'


if __name__ == "__main__":
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    app.run(host='localhost', port=8080, threaded=True, debug=True)





