from flask import Flask, session, request, jsonify, render_template
from psn import PSNSession, get_npsso
from model import create_tables, db, User, Device
from functools import wraps
import pickle
from util import request_needs

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTABCOK'

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(resp):
    db.close()
    return resp

@app.route('/sso', methods=['GET'])
@request_needs('username', 'password', in_='args')
def get_sso(username, password):
    return get_npsso(username, password)

@app.route('/register_device', methods=['GET'])
@request_needs('sso', 'apns_token', in_='args')
def register_device(sso, apns_token):
    # get an existing user or create a new one
    user = User.get_or_create(sso=sso)[0]
    # create the device if it doesn't already exist
    _, created = Device.create_or_get(apns_token=apns_token)
    response = "registered device!" if created else "device already registered!"
    return render_template('plain.html', content=response)

@app.route('/friends', methods=['GET'])
@request_needs('sso', in_='args')
def friends(sso):
    psn_session.get_tokens()
    return 'ok'
    # session['psn_session'].get_tokens()
    # return jsonify(session['psn_session'].get_friends())

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
