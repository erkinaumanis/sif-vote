from datetime import datetime, timedelta
from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, jsonify, Blueprint
from wtforms import Form, BooleanField, TextField, validators, ValidationError
# from models import get_all_pitches, create_pitch, create_action, get_pitch_actions, get_all_actions, \
#                     get_recent_numbers, get_all_pitches, vote_on_action, get_active_pitches
from app import app
import twilio.twiml
from twilio.rest import TwilioRestClient
from lib import tokens
import json
import pdb
import sys

client = TwilioRestClient(tokens.TWILIO_ID, tokens.TWILIO_TOKEN)

views = Blueprint('views',__name__)

# Renders page for dashboard and current pitches
@views.route('/', methods=['GET'])
def index():
    from models import get_active_pitches
    active_pitches = get_active_pitches()
    return render_template('dashboard.html', stocks=active_pitches)

# Renders page for latest pitch, basically a copy of current
@views.route('/latest', methods=['GET'])
def latest():
    from models import get_all_pitches
    # TODO: change to current pitches
    pitches = get_all_pitches()
    return render_template('latest.html', stocks=pitches)

# Renders form for new pitches
@views.route('/new', methods=['GET'])
def new():
    return render_template('new.html')

# Takes in form data for new pitches
@views.route('/create', methods=['POST'])
def create():
    from models import get_all_pitches, create_action, create_pitch
    if request.method == "POST":
        data = request.form

        # take out $ sign in 
        data['amount-1'].replace('$',"")
        data['amount-2'].replace('$',"")

        # add new pitches and actions to mongo
        create_pitch(data['pitch-name'], data['ticker'], data['pitch-date'])
        create_action(data['symbol-1'], data['pitch-name'], data['action-1'], data['amount-1'], data['ticker'])
        create_action(data['symbol-2'], data['pitch-name'], data['action-2'], data['amount-2'], data['ticker'])

        pitches = get_all_pitches()
        
        return render_template('list.html', stocks=pitches)

# Renders page to view all pitches
@views.route('/all', methods=['GET'])
def all():
    from models import get_all_pitches
    pitches = get_all_pitches()
    return render_template('list.html', stocks=pitches)

# Renders page for an individual vote result from all votes
@views.route('/vote/<string:ticker>', methods=['GET'])
def vote(ticker):
    from models import get_pitch_actions
    # TODO: Make this return all stocks for a given pitch
    # vote_stocks = _filter_unique(stocks, stock_id)
    vote_stocks = get_pitch_actions(ticker)
    return render_template('display.html', stocks=vote_stocks)


# Route to receive texts from twilio
@views.route('/recieve', methods=['POST'])
def recieve():
    from models import vote_on_action, is_number_voted
    if request.method == "POST":

        print "request: ", request
        print "request.values: ", request.values

        print "from: ", request.values.get('From')
        print "body: ", request.values.get('Body')

        if request.values.get('From'):
            number = request.values.get('From')
        else:
            number = request.json['From']

        if request.values.get('Body'):
            symbol = str(request.values.get('Body'))
        else:
            symbol = str(request.json['Body'])

        sys.stdout.flush()

        # number exists
        if is_number_voted(symbol,number):
            client.sms.messages.create(to=number, from_=tokens.TWILIO_NUM, body='Thanks, but you already voted!')
        else:
            vote_on_action(symbol, number)
            client.sms.messages.create(to=number, from_=tokens.TWILIO_NUM, body='Thanks for your vote!')
  
    return jsonify(request.form)

# Returns json to update graphs
@views.route('/update_votes', methods=['GET'])
def update_votes():
    from models import get_active_pitches
    ap = get_active_pitches()
    ap_dict = {}
    for p in ap:
        a_dict = {}
        for a in p[1]:
            a_dict[a.action_id] = a.vote_count
        ap_dict[p[0].ticker] = a_dict
    return jsonify(ap_dict)

# Returns json to update recent vote numbers
@views.route('/update_numbers', methods=['GET'])
def update_numbers():
    from models import get_recent_numbers
    rv = get_recent_numbers()    
    rv_dict = {}    
    for i,n in enumerate(rv):
        rv_dict[i] = n
    return jsonify(rv_dict)


def _filter_unique(stocks, stock_id):
    vote_stocks = []
    for s in stocks:
        if stock_id == s["id"] or s["id"] == stock_id + 1:
            vote_stocks.append(s)
    return vote_stocks