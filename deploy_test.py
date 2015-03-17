#!/usr/bin/env python3


import datetime

from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return '''
        <h1>Welcome</h1>
        <p>Right now it is {}.</p>
        <p>Play with setting values in a <a href="/session/">Session</a>.</p>
        '''.format(datetime.datetime.now())


if __name__ == '__main__':
    app.run()
