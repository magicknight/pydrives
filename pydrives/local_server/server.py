#!/usr/bin/env python3
from flask import request
from flask import Flask
import redis
from pydrives.config import config

app = Flask(__name__)


@app.route("/")
def get_auth_key():
    refresh_token = request.args.get('state')
    auth_token = request.args.get('code')
    r.set(refresh_token, auth_token)
    return 'You are authorized'


if __name__ == "__main__":
    r = redis.StrictRedis(host=config['redis']['host'], port=config['redis']['port'], db=config['redis']['db'])
    app.run(host=config['redirect']['host'], port=config['redirect']['port'], threaded=True, debug=True)





