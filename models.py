from datetime import datetime
from app import db

#---------------------------------------------
# model class schema
# --------------------------------------------

class Pitch(db.DynamicDocument):
    ''' class to hold the data of a particular pitch the fund is voting on '''

    # TODO: add in other field params
    pitch_date = db.StringField()
    status = db.StringField(max_length=10, default="active")
    name = db.StringField(max_length=25)
    ticker = db.StringField(max_length=5)
    created_at = db.DateTimeField(default=datetime.now()) 

class Action(db.DynamicDocument):
    ''' class to hold the different possible actions of a pitch '''

    # TODO: add in other field params
    name = db.StringField(max_length=25)
    vote_count = db.IntField(default = 0)
    vote_numbers = db.ListField()
    vote_symbol = db.StringField(max_length=1)
    ticker = db.StringField(max_length=5)
    action = db.StringField(max_length=40)
    amount = db.IntField()
    action_id = db.IntField()
    created_at = db.DateTimeField(default=datetime.now())
    

#---------------------------------------------
# model layer actions
# --------------------------------------------

# TODO: add more model layer actions
def create_pitch(name, ticker, date):
    new_pitch = Pitch()
    new_pitch.name = name
    new_pitch.ticker = ticker
    new_pitch.pitch_date = date
    new_pitch.is_active = True
    new_pitch.save()

def create_action(symbol, name, action, amount, ticker):
    # TODO: ADD ATOMIC INCREMENT
    new_action = Action()
    new_action.symbol = symbol
    new_action.name = name
    new_action.action = action
    new_action.amount = amount
    new_action.ticker = ticker
    new_action.save()

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

    if pitch_actions is not None:
        action = [a for a in pitch_actions if a.symbol == symbol]
        votes = action[0].vote_count + 1
        action[0].update(set__vote_count = votes)
    # numbers = action[0].numbers
    # action.update(set__numbers = action.numbers)
