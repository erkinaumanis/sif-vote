from datetime import datetime, timedelta
from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, jsonify
from wtforms import Form, BooleanField, TextField, validators, ValidationError
from models import get_all_pitches, create_pitch, create_action, get_pitch_actions, get_all_actions, get_all_pitches, vote_on_action, get_active_pitches
from app import app
import twilio.twiml
from twilio.rest import TwilioRestClient
from lib import tokens
import pdb

client = TwilioRestClient(tokens.TWILIO_ID, tokens.TWILIO_TOKEN)

# Renders page for dashboard and current pitches
@app.route('/', methods=['GET'])
def index():
    active_pitches = get_active_pitches()
    return render_template('dashboard.html', stocks=active_pitches)

# Renders page for latest pitch, basically a copy of current
@app.route('/latest', methods=['GET'])
def latest():
    # TODO: change to current pitches
    pitches = get_all_pitches()
    return render_template('latest.html', stocks=pitches)

# Renders form for new pitches
@app.route('/new', methods=['GET'])
def new():
    return render_template('new.html')

# Takes in form data for new pitches
@app.route('/create', methods=['POST'])
def create():
    if request.method == "POST":
        data = request.form

        # add new pitches and actions to mongo
        create_pitch(data['pitch-name'], data['ticker'], data['pitch-date'])
        create_action(data['symbol-1'], data['pitch-name'], data['action-1'], data['amount-1'], data['ticker'])
        create_action(data['symbol-2'], data['pitch-name'], data['action-2'], data['amount-2'], data['ticker'])

        pitches = get_all_pitches()
        
        return render_template('list.html', stocks=pitches)

# Renders page to view all pitches
@app.route('/all', methods=['GET'])
def all():
    pitches = get_all_pitches()
    return render_template('list.html', stocks=pitches)

# Renders page for an individual vote result from all votes
@app.route('/vote/<string:ticker>', methods=['GET'])
def vote(ticker):
    # TODO: Make this return all stocks for a given pitch
    # vote_stocks = _filter_unique(stocks, stock_id)
    vote_stocks = get_pitch_actions(ticker)
    return render_template('display.html', stocks=vote_stocks)

# Route to receive texts from twilio
@app.route('/recieve', methods=['POST'])
def recieve():
    if request.method == "POST":

        number = request.values.get('From')

        # number exists
        # if number in numbers:
        #     client.sms.messages.create(to=number, from_=TWILIO_NUM, body='Thanks, but you already voted!')
        # else:
        # sweet
        body = request.values.get('Body').upper()            
        ticker = body.rsplit(" ", 1)[1]
        symbol = body.rsplit(" ", 1)[0]
        valid = False

        vote_on_action(ticker, symbol, number)
        client.sms.messages.create(to=number, from_=tokens.TWILIO_NUM, body='Thanks for your vote!')


        #     if s["decision"].lower() == vote and s["ticker"].lower() == ticker:
        #         s["votes"] += 1
        #         numbers.add(number)
        #         valid = True
        #         client.sms.messages.create(to=number, from_=TWILIO_NUM, body='Thanks for your vote!')
        #         break
        # for s in stocks:

        # if valid == False:
        #     client.sms.messages.create(to=number, from_=TWILIO_NUM, body='That is an invalid vote, please try again!')
    return jsonify(request.form)

# Returns json to update graphs
@app.route('/update', methods=['GET'])
def update():
    ap = get_active_pitches()
    ap_dict = {}
    for p in ap:
        a_dict = {}
        for a in p[1]:
            a_dict[a.action_id] = a.vote_count
        ap_dict[p[0].ticker] = a_dict
    return jsonify(ap_dict)


def _filter_unique(stocks, stock_id):
    vote_stocks = []
    for s in stocks:
        if stock_id == s["id"] or s["id"] == stock_id + 1:
            vote_stocks.append(s)
    return vote_stocks