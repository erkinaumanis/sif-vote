import os
from flask import Flask, request, redirect, g, render_template, jsonify
from lib import tokens
import twilio.twiml
import logging
import pdb


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


connect('claremont-sms-db', host='mongodb://' + 'evan' + ':' + tokens.DB_PASSWORD + '@' + tokens.DB_HOST_ADDRESS)
client = TwilioRestClient(tokens.TWILIO_ID, tokens.TWILIO_TOKEN)

stocks = [
{"id": 0, "ticker": "CAT", "name": "Caterpillar", "action": "Buy", "amount": "$10,000", "status": "Active", "date": "10/29", "decision": "Buy", "votes": 0, "result": None},
{"id": 1, "ticker": "CAT", "name": "Caterpillar", "action": "Don't Buy", "amount": "N/A", "status": "Active", "date": "10/29", "decision": "Don't Buy", "votes": 0, "result": None},
{"id": 2, "ticker": "PM", "name": "Phillip Morris", "action": "Buy", "amount": "$15,000", "status": "Active", "date": "10/29", "decision": "Buy", "votes": 0, "result": None},
{"id": 3, "ticker": "PM", "name": "Phillip Morris", "action": "Don't Buy", "amount": "N/A", "status": "Active", "date": "10/29", "decision": "Don't Buy", "votes": 0, "result": None},
]

@app.route('/')
def index():
    unique_stocks = []
    for s in stocks:
        if s["id"] % 2 == 0:
            unique_stocks.append(s)
    return render_template('list.html', stocks=unique_stocks)

@app.route('/list')
def list():
    return jsonify(stocks=stocks)

@app.route('/vote/<int:stock_id>')
def display(stock_id):
    vote_stocks = []
    for s in stocks:
        if stock_id == s["id"] or s["id"] == stock_id + 1:
            vote_stocks.append(s)
    return render_template('display.html', stocks=vote_stocks)

@app.route('/vote', methods=['POST'])
def vote():
    if request.method == "POST":
        number = request.form['From']
        # number exists
        if from_number in numbers:
            client.sms.messages.create(to=number, from_=tokens.TWILIO_NUM, body='Thanks, but you already voted!')
        else:
            body = request.form['Body'].lower()
            letters = "ABCDEFGHIJKLMNOP"
            if len(body) != 1 or ident == -1 or ident >= len(projects):
                client.sms.messages.create(to=number, from_=tokens.TWILIO_NUM, body='That is an invalid vote, please try again!')
            else:
                ticker = body.rsplit(" ", 1)[0]
                vote = body.rsplit(" ", 1)[1]
                for s in stocks:
                    if s["decision"] == vote and s["ticker"] == ticker:
                        s["votes"] += 1
                        break
                    else:
                        client.sms.messages.create(to=number, from_=tokens.TWILIO_NUM, body='That is an invalid vote, please try again!')
                numbers.add(from_number)
                client.sms.messages.create(to=number, from_=tokens.TWILIO_NUM, body='Thanks for your vote!')
    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
