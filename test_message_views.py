"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.testuser2 = User.signup(username="testuser2",
                                    email="test2@test.com",
                                    password="testuser",
                                    image_url=None)
        self.testuser2_id = 9999
        self.testuser2.id = self.testuser2_id


        db.session.commit()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp


    def test_add_message(self):
        """Can user add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def test_no_session(self):
        with self.client as c:
            resp = c.post("/messages/new", data={"text": "Hello"})
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

    def test_add_invalid_user(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 99222224 # user does not exist

            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

    def test_message_show(self):

        testuser_id = self.testuser_id
        testuser2_id = self.testuser2_id

        m = Message(
            id=1234,
            text="a test message",
            user_id=self.testuser_id
        )
        
        db.session.add(m)
        db.session.commit()

        with self.client as c:

            #m = Message.query.get(1234)
            
            # not logged in redirect
            resp = c.get(f'/messages/{m.id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Delete", html)

            # Assign session, we're logged in now!
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = testuser_id
            

            resp = c.get(f'/messages/{m.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(m.text, str(resp.data))
            self.assertIn("Delete", str(resp.data))

            #login as other user
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = testuser2_id

            resp = c.get(f'/messages/{m.id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # Not own message should not show Delete button
            self.assertNotIn('Delete' , html)

    def test_invalid_message_show(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get('/messages/99999999')

            self.assertEqual(resp.status_code, 404)

    
    def test_message_delete(self):

        testuser_id = self.testuser_id
        testuser2_id = self.testuser2_id

        m = Message(
            id=1234,
            text="a test message",
            user_id=self.testuser_id
        )
        
        db.session.add(m)
        db.session.commit()

        with self.client as c:

            #not logged in redirect, can not delete, redirect to homepage
            resp = c.post(f'/messages/{m.id}/delete')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/')

            #login as other user, can not delete, redirect to user
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = testuser2_id

            resp = c.post(f'/messages/{m.id}/delete')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/')

            # Login as the correct user, try to delete
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = testuser_id

            resp = c.post(f'/messages/{m.id}/delete')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f'http://localhost/users/{testuser_id}')