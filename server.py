import os
from flask import Flask, request, redirect, g, render_template, jsonify
import twilio.twiml
import logging
import pdb


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


numbers = set()
stocks = [
{"id": 0, "name": "Caterpillar", "action": "Buy", "amount": "$10,000", "status": "Active", "date": "10/29", "votes":0, "result": None},
{"id": 1, "name": "Caterpillar", "action": "Don't Buy", "amount": "N/A", "status": "Active", "date": "10/29", "votes":0, "result": None},
{"id": 2, "name": "Phillip Morris", "action": "Buy", "amount": "$15,000", "status": "Active", "date": "10/29", "votes":0, "result": None},
{"id": 3, "name": "Phillip Morris", "action": "Don't Buy", "amount": "N/A", "status": "Active", "date": "10/29", "votes":0, "result": None},
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
    from_number = request.form['From']
    # number exists
    resp = twilio.twiml.Response()
    if from_number in numbers:
        resp.sms("Thanks, but you already voted!")
    else:
        body = request.form['Body'].strip()
        letters = "ABCDEFGHIJKLMNOP"
        ident = letters.find(body)
        if len(body) != 1 or ident == -1 or ident >= len(projects):
            resp.sms('That is an invalid vote, please try again!')
        else:
            stocks[ident]['votes'] += 1
            numbers.add(from_number)
            resp.sms('Thank you for your vote!')
    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
