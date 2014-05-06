from datetime import datetime, timedelta
from app.database import Database
from random import randint
import pdb

#---------------------------------------------
# model class schema
# --------------------------------------------

class Pitch(Database().DynamicDocument):
    ''' class to hold the data of a particular pitch the fund is voting on '''

    pitch_date = Database().StringField()
    status = Database().StringField(max_length=10, default="active")
    name = Database().StringField(max_length=500)
    ticker = Database().StringField(max_length=50)
    created_at = Database().DateTimeField(default=datetime.now()) 

class Action(Database().DynamicDocument):
    ''' class to hold the different possible actions of a pitch '''
    
    name = Database().StringField(max_length=500)
    vote_count = Database().IntField(default=0)
    vote_numbers = Database().ListField()
    vote_symbol = Database().StringField(max_length=10)
    ticker = Database().StringField(max_length=50)
    action = Database().StringField(max_length=50)
    amount = Database().IntField()
    action_id = Database().IntField()
    created_at = Database().DateTimeField(default=datetime.now())

class Vote(Database().DynamicDocument):
    ''' class to store vote data '''

    number = Database().IntField()
    symbol = Database().StringField(max_length=5)
    ticker = Database().StringField(max_length=40)
    created_at = Database().DateTimeField(default=datetime.now())
    

#---------------------------------------------
# model layer actions
# --------------------------------------------

def create_pitch(name, ticker, date):
    ''' create and save a new pitch object '''
    new_pitch = Pitch()
    new_pitch.name = name
    new_pitch.ticker = ticker
    new_pitch.pitch_date = date
    new_pitch.save()

def create_action(name, action, amount, ticker):
    ''' create and save a new action object '''
    new_action = Action()
    new_action.symbol = generate_symbol()
    new_action.name = name
    new_action.action = action
    new_action.amount = amount
    new_action.ticker = ticker
    new_action.action_id = randint(0,1000)
    new_action.save()

def create_vote(number, symbol, ticker):
    ''' create and save a new vote object '''
    new_vote = Vote()
    new_vote.number = number
    new_vote.symbol = symbol
    new_vote.ticker = ticker
    new_vote.save()

def generate_symbol():
    ''' generates a unique random integer to use as the action's symbol '''
    
    symbol = str(randint(1000,9999))
    active_pitches = list(Pitch.objects(status="active"))
    active_symbols = []
    for pitch in active_pitches:
        actions = list(Action.objects(name=pitch.name))
        active_symbols += [action.symbol for action in actions]

    while symbol in active_symbols:
        symbol = str(randint(1000,9999))

    return symbol

def get_all_pitches():
    ''' returns a list of all pitch objects '''
    return list(Pitch.objects())

def get_all_actions():
    ''' returns a list of all action objects '''
    return list(Action.objects())

def get_pitch_data_by_ticker(ticker):
    ''' returns the pitch and corresponding actions with user provided ticker if exists, 
        if not returns an empty list '''
    ticker_pitches=list(Pitch.objects(ticker=ticker))
    return [(p,get_pitch_actions(p.ticker)) for p in ticker_pitches]

def get_pitch_by_ticker(ticker):
    ''' returns the pitch with user provided ticker if exists, if not returns an empty list '''
    return list(Pitch.objects(ticker=ticker))

def get_pitch_actions(ticker):
    ''' returns a list of action objects corresponding to specified ticker '''
    return list(Action.objects(ticker = ticker))

def vote_on_action(symbol, number):
    ''' increments count and adds number to vote and returns true if valid symbol,
        false if symbol is invalid'''
    active_pitches = list(Pitch.objects(status="active"))
    active_actions = []
    for pitch in active_pitches:
        active_actions += list(Action.objects(name=pitch.name,symbol=symbol))

    ticker = active_actions[0].ticker

    if len(active_actions) != 0:
        votes = active_actions[0].vote_count + 1
        active_actions[0].update(set__vote_count = votes) # update action class
        create_vote(number,symbol,ticker) # update vote class

def get_active_pitches():
    ''' returns a list of active pitches '''
    active_pitches = list(Pitch.objects(status="active"))
    return [(p,get_pitch_actions(p.ticker)) for p in active_pitches]

def get_recent_numbers():
    ''' returns a formatted list of all recent vote numbers '''
    active_pitches = list(Pitch.objects(status="active"))
    if len(active_pitches) > 0:
        ticker = active_pitches[0].ticker
        active_votes = list(Vote.objects(ticker=ticker))
        recent_votes = [v for v in active_votes if (v.created_at - datetime.utcnow()) < timedelta(hours=24)]    
        return ["("+str(v.number)[1:4]+") "+str(v.number)[4:7]+"-"+str(v.number)[7:11]+" has voted!" for v in recent_votes]
    else:
        return []

def is_number_voted(symbol,number):
    ''' returns true if number has voted on symbol's pitch, false if number has not '''
    ticker = Action.objects(symbol=symbol)[0].ticker
    ticker_votes = Vote.objects(ticker=ticker)
    for votes in ticker_votes:
        if votes.number == number:
            return True
    return False

def is_symbol_valid(symbol):
    ''' returns true if symbol corresponds to valid, active action, false if not '''
    symbol_actions = list(Action.objects(symbol=symbol))

    if len(symbol_actions) == 0:
        return False
    else:
        ticker = symbol_actions[0].ticker
        active_pitches = list(Pitch.objects(ticker=ticker,status="active"))

        if len(active_pitches) == 0:
            return False

    return True
