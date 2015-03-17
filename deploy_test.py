#!/usr/bin/env python3


import datetime
import os

from flask import Flask, session, redirect, request, url_for


PREFIX = 'deploy.'


app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return '''
        <h1>Welcome</h1>
        <p>Right now it is {}.</p>
        <p>Play with setting values in a <a href="{}">Session</a>.</p>
        '''.format(datetime.datetime.now(), url_for('session_'))


def get_deploy_keys():
    plen = len(PREFIX)
    return {
        k[plen:]: v
        for (k, v) in session.items()
        if k.startswith(PREFIX)
        }


@app.route('/session/', methods=['POST', 'GET'])
def session_():
    key = request.form.get('key')
    if key:
        session[PREFIX + key] = request.form.get('value')

    cookie = get_deploy_keys()

    if cookie:
        buf = ['<h2>Current Cookies</h2>\n<ul>']
        for (k, v) in cookie.items():
            buf.append("<li><b>{}</b>: '{}'</li>".format(k, v))
        buf.append('</ul>')
        output = '\n'.join(buf)
    else:
        output = '<p>The cookie jar is empty. :( </p>'

    return '''
        <h1>Sessions</h1>
        {}
        <form method="POST" action="{}">
            <label for="key">Key</label>
            <input type="input" name="key" />

            <label for="value">Value</label>
            <input type="input" name="value" />

            <input type="submit" />
        </form>
        <p><a href="{}">EAT ALL THE COOKIES!</a></p>
        <p>Return to <a href="{}">Home</a>.</p>
        '''.format(output, url_for('session_'), url_for('clear'),
                   url_for('index'))


@app.route('/clear/')
def clear():
    for k in session.keys():
        if k.startswith(PREFIX):
            del session[k]
    return redirect(url_for('session_'))


@app.route('/about/')
def about():
    pass


if __name__ == '__main__':
    app.run()
