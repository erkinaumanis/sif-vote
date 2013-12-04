from datetime import datetime, timedelta
from app import db
from random import randint
import pdb

#---------------------------------------------
# model class schema
# --------------------------------------------

class Pitch(db.DynamicDocument):
    ''' class to hold the data of a particular pitch the fund is voting on '''

    # TODO: add in other field params
    pitch_date = db.StringField()
    status = db.StringField(max_length=10, default="active")
    name = db.StringField(max_length=40)
    ticker = db.StringField(max_length=5)
    created_at = db.DateTimeField(default=datetime.now()) 

class Action(db.DynamicDocument):
    ''' class to hold the different possible actions of a pitch '''
    
    name = db.StringField(max_length=25)
    vote_count = db.IntField(default = 0)
    vote_numbers = db.ListField()
    vote_symbol = db.StringField(max_length=1)
    ticker = db.StringField(max_length=5)
    action = db.StringField(max_length=40)
    amount = db.IntField()
    action_id = db.IntField()
    created_at = db.DateTimeField(default=datetime.now())

class Vote(db.DynamicDocument):
    ''' class to store vote data '''

    number = db.IntField()
    symbol = db.StringField(max_length=5)
    ticker = db.StringField(max_length=40)
    created_at = db.DateTimeField(default=datetime.now())
    

#---------------------------------------------
# model layer actions
# --------------------------------------------

def create_pitch(name, ticker, date):
    new_pitch = Pitch()
    new_pitch.name = name
    new_pitch.ticker = ticker
    new_pitch.pitch_date = date
    new_pitch.is_active = True
    new_pitch.save()

def create_action(symbol, name, action, amount, ticker):
    new_action = Action()
    new_action.symbol = symbol
    new_action.name = name
    new_action.action = action
    new_action.amount = amount
    new_action.ticker = ticker
    new_action.action_id = randint(0,1000)
    new_action.save()

def create_vote(number, symbol, ticker):
    new_vote = Vote()
    new_vote.number = number
    new_vote.symbol = symbol
    new_vote.ticker = ticker
    new_vote.save()

def get_all_pitches():
    return list(Pitch.objects())

def get_all_actions():
    return list(Action.objects())

def get_pitch_actions(ticker):
    # returns pitch data + actions
    return list(Action.objects(ticker = ticker))

def vote_on_action(ticker, symbol, number):
    # increments count and adds number to vote
    
    pitch_actions = list(Action.objects(ticker = ticker))

    # update action class
    if pitch_actions is not None:
        action = [a for a in pitch_actions if a.symbol == symbol]
        votes = action[0].vote_count + 1
        action[0].update(set__vote_count = votes)

    # update vote class
    create_vote(number,symbol,ticker)

def get_active_pitches():
    all_pitches = list(Pitch.objects())
    active_pitches = [p for p in all_pitches if p.status == 'active']
    return [(p,get_pitch_actions(p.ticker)) for p in active_pitches]

def get_recent_numbers():
    all_votes = list(Vote.objects())
    recent_votes = [v for v in all_votes if (v.created_at - datetime.utcnow()) < timedelta(hours=24)]    
    return ["("+str(v.number)[1:4]+") "+str(v.number)[4:7]+"-"+str(v.number)[7:11]+" has voted!" for v in recent_votes]