from datetime import datetime, timedelta
from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, jsonify, Blueprint
from app import app
import twilio.twiml
from twilio.rest import TwilioRestClient
from lib import tokens,forms
import json
import pdb
import sys
import json

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

@views.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

# Processes form data for new pitches
@views.route('/create', methods=['POST'])
def create():
    from models import get_all_pitches, create_action, create_pitch

    if request.method == "POST":

        data = request.form
        amount1,amount2 = forms.preprocess_new_pitch(data)  

        # add new pitches and actions to mongo
        create_pitch(data['pitch-name'], data['ticker'], data['pitch-date'])
        create_action(data['pitch-name'], data['action-1'], amount1, data['ticker'])
        create_action(data['pitch-name'], data['action-2'], amount2, data['ticker'])

        pitches = get_all_pitches()
        
        return render_template('list.html', stocks=pitches)

# Renders page to view all pitches
@views.route('/all', methods=['GET'])
def all():
    from models import get_all_pitches
    pitches = get_all_pitches()
    pitches.sort(key=lambda x: x.created_at,reverse=True)    
    return render_template('list.html', stocks=pitches)

# Renders page for an individual vote result from all votes
@views.route('/vote/<string:ticker>', methods=['GET'])
def vote(ticker):
    from models import get_pitch_data_by_ticker
    vote_pitches = get_pitch_data_by_ticker(ticker)
    return render_template('display.html', stocks=vote_pitches)

@views.route('/delete/<string:ticker>', methods=['GET'])
def delete(ticker):
    from models import delete_pitch, get_all_pitches
    delete_pitch(ticker)
    pitches = get_all_pitches()
    pitches.sort(key=lambda x: x.created_at,reverse=True)   
    return render_template('list.html', stocks=pitches)
    
@views.route('/update/<string:ticker>', methods=['GET'])
def update(ticker):
    from models import update_pitch_status, get_all_pitches
    update_pitch_status(ticker)
    pitches = get_all_pitches()
    pitches.sort(key=lambda x: x.created_at,reverse=True)  
    return render_template('list.html', stocks=pitches)

# Route to receive texts from twilio
@views.route('/recieve', methods=['POST'])
def recieve():
    from models import vote_on_action, is_number_voted, is_symbol_valid
    if request.method == "POST":   

        if request.values.get('From'):
            number = int(request.values.get('From'))
        else:
            number = int(json.loads(request.values.keys()[0])["From"])

        if request.values.get('Body'):
            symbol = str(request.values.get('Body'))
        else:
            symbol = str(json.loads(request.values.keys()[0])["Body"])

        # number exists
        if is_symbol_valid(symbol) is False:
            print "invalid symbol"
            client.sms.messages.create(to=number, from_=tokens.TWILIO_NUM, body='Invalid symbol, try again!')            
        elif is_number_voted(symbol,number):
            print "already voted"
            client.sms.messages.create(to=number, from_=tokens.TWILIO_NUM, body='Thanks, but you already voted!')
        else:
            print "valid"
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

@views.route('/vote/<string:ticker>/update_votes', methods=['GET'])
def view(ticker):
    from models import get_pitch_data_by_ticker
    ap = get_pitch_data_by_ticker(ticker)
    ap_dict = {}
    for p in ap:
        a_dict = {}
        for a in p[1]:
            a_dict[a.action_id] = a.vote_count
        ap_dict[p[0].ticker] = a_dict
    return jsonify(ap_dict)

