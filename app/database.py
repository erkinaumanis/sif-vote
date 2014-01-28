import sys
from lib import tokens
import pdb

from mongoengine import connect
from flask.ext.mongoengine import MongoEngine

class Database(object):
    __db = None

    def __new__(cls, **kwargs):

        if cls.__db is None:
            try:           
                connect(kwargs['app'].config['MONGODB_DB'], host='mongodb://' + tokens.DB_USER + ':' + tokens.DB_PASSWORD + '@' + kwargs['app'].config['MONGODB_HOST'])
                cls.__db = MongoEngine(kwargs['app'])
            except:
                print "Cannot connect to mongo test server.  Exiting..."
                sys.exit(0)

        return cls.__db

def get_test_db():
    return Redis(host='localhost', port=6379, db=1)