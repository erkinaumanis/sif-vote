import os
from flask import Flask, request, redirect, g, render_template, jsonify
import twilio.twiml
from twilio.rest import TwilioRestClient
import logging
import pdb

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)

TWILIO_NUM = "+13038163058"
TWILIO_ID = "ACfdd41e08b900b330579f39feb9366f4d"
TWILIO_TOKEN = "d951d114074f6d3aeb672672383f8ab3"

client = TwilioRestClient(TWILIO_ID, TWILIO_TOKEN)

numbers = set()
stocks = [
{"id": 0, "ticker": "CAT", "name": "Caterpillar", "action": "Buy", "amount": "$10,000", "status": "Active", "date": "10/29", "decision": "Buy", "votes": 3, "result": None},
{"id": 1, "ticker": "CAT", "name": "Caterpillar", "action": "Don't Buy", "amount": "N/A", "status": "Active", "date": "10/29", "decision": "Don't Buy", "votes": 0, "result": None},
{"id": 2, "ticker": "PM", "name": "Phillip Morris", "action": "Buy", "amount": "$15,000", "status": "Active", "date": "10/29", "decision": "Buy", "votes": 0, "result": None},
{"id": 3, "ticker": "PM", "name": "Phillip Morris", "action": "Don't Buy", "amount": "N/A", "status": "Active", "date": "10/29", "decision": "Don't Buy", "votes": 0, "result": None},
]

@app.route('/', methods=['GET'])
def index():
    unique_stocks = []
    for s in stocks:
        if s["id"] % 2 == 0:
            unique_stocks.append(s)
    return render_template('list.html', stocks=unique_stocks)

@app.route('/list', methods=['GET'])
def list():
    print "here"
    return jsonify(stocks=stocks)

@app.route('/vote/<int:stock_id>', methods=['GET'])
def vote(stock_id):
    vote_stocks = []
    for s in stocks:
        if stock_id == s["id"] or s["id"] == stock_id + 1:
            vote_stocks.append(s)
    return render_template('display.html', stocks=vote_stocks)

@app.route('/recieve', methods=['POST'])
def recieve():
    print "here"
    if request.method == "POST":
        number = request.values.get("From")

        # number exists
        if number in numbers:
            client.sms.messages.create(to=number, from_=TWILIO_NUM, body='Thanks, but you already voted!')
        else:
            body = request.values.get('Body').lower()            
            ticker = body.rsplit(" ", 1)[1]
            vote = body.rsplit(" ", 1)[0]
            for s in stocks:
                if s["decision"].lower() == vote and s["ticker"].lower() == ticker:
                    s["votes"] += 1
                    numbers.add(from_number)
                    client.sms.messages.create(to=number, from_=TWILIO_NUM, body='Thanks for your vote!')
                    break
            client.sms.messages.create(to=number, from_=TWILIO_NUM, body='That is an invalid vote, please try again!')
    return jsonify(request.form)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
