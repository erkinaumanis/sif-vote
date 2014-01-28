# import unittest
# import os
# import tempfile
# import time
# import pdb
 
# from mongoengine import *

# from app import *
# from lib import tokens

# class BasicTestCase(unittest.TestCase):

#     def test_index(self):
#         """Inital test. ensure flask was set up correctly"""
#         tester = app.test_client(self)
#         response = tester.get('/', content_type='html/text')
#         self.assertEqual(response.status_code, 200)


# class MongoTestCase(unittest.TestCase):

#     def setUp(self):
#         """Set up a blank temp database before each test"""
#         self.db_name = 'test_sif_vote'
#         app.config['MONGODB_DB'] = self.db_name
#         app.config['TESTING'] = True
#         self.app = app
#         self.db = MongoEngine()
#         self.db.init_app(app)

#     # def tearDown(self):
#     #     """Destroy blank temp database after each test"""
#     #     os.close(self.db_fd)
#     #     os.unlink(app.app.config['DATABASE'])

#     # def login(self, username, password):
#     #     """Login helper function"""
#     #     return self.app.post('/login', data=dict(
#     #         username=username,
#     #         password=password
#     #     ), follow_redirects=True)

#     # def logout(self):
#     #     """Logout helper function"""
#     #     return self.app.get('/logout', follow_redirects=True)

#     # # assert functions

#     def test_empty_db(self):
#         """Ensure database is blank"""
#         c = self.app.test_client()
#         resp = c.get('/')
#         self.assertEqual(resp.status_code, 200)
#         self.assertEquals(resp.data.decode('utf-8'), 'hello session')
    
#     # def test_login_logout(self):
#     #     """Test login and logout using helper functions"""
#     #     rv = self.login(app.app.config['USERNAME'], app.app.config['PASSWORD'])
#     #     self.assertIn(b'You were logged in', rv.data)
#     #     rv = self.logout()
#     #     self.assertIn(b'You were logged out', rv.data)
#     #     rv = self.login(app.app.config['USERNAME'] + 'x', app.app.config['PASSWORD'])
#     #     self.assertIn(b'Invalid username', rv.data)
#     #     rv = self.login(app.app.config['USERNAME'], app.app.config['PASSWORD'] + 'x')
#     #     self.assertIn(b'Invalid password', rv.data)

#     # def test_messages(self):
#     #     """Ensure that user can post messages"""
#     #     self.login(app.app.config['USERNAME'], app.app.config['PASSWORD'])
#     #     rv = self.app.post('/add', data=dict(
#     #         title='<Hello>',
#     #         text='<strong>HTML</strong> allowed here'
#     #     ), follow_redirects=True)
#     #     self.assertNotIn(b'No entries here so far', rv.data)
#     #     self.assertIn(b'&lt;Hello&gt;', rv.data)
#     #     self.assertIn(b'<strong>HTML</strong> allowed here', rv.data)


# if __name__ == '__main__':
#     unittest.main()