from datetime import datetime
from app import db

#---------------------------------------------
# model class schema
# --------------------------------------------

class Pitch(db.DynamicDocument):
    ''' class to hold the data of a particular pitch the fund is voting on '''

    # TODO: add in other field params
    pitch_date = db.DateTimeField()
    is_active = db.BooleanField()
    actions = db.ListField()
    name = db.StringField(max_length=25)
    ticker = db.StringField(max_length=5)
    created_at = db.DateTimeField(default=datetime.now()) 

class Action(db.DynamicDocument):
    ''' class to hold the different possible actions of a pitch '''

    # TODO: add in other field params
    vote_count = db.IntField()
    vote_numbers = db.ListField()
    vote_symbol = db.StringField(max_length=1)
    action = db.StringField(max_length=40)
    amount = db.IntField()
    created_at = db.DateTimeField(default=datetime.now())
    

#---------------------------------------------
# model layer actions
# --------------------------------------------

# TODO: add model layer actions
