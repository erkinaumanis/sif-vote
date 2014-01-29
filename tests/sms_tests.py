import os 
import sys
import pdb
import unittest
import tempfile
import time
import subprocess
import signal

sys.path.insert(0, '../')
from app import *

class SMSUnitTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        from app import config
        self.app = start_app(config.Test)
        
        # connect to the test db    
        from mongoengine.connection import connect, disconnect, get_connection
        disconnect()
        from app.database import Database
        self.db = Database(app=self.app)
        
    @classmethod
    def tearDownClass(self):  
        from mongoengine.connection import connect, disconnect, get_connection
        connection = get_connection()
        connection.drop_database('test-sif-vote')

class SMSTest(SMSUnitTest):

    def setUp(self):
        pass

    def test_empty_db(self):
        ''' Ensure database is blank '''

        c = self.app.test_client()
        resp = c.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_vote(self):
        pass

if __name__ == '__main__':
    unittest.main() 