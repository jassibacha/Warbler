"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follows , Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test Message Model."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 9999
        u = User.signup("testing", "testing@test.com", "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_message_model(self):
        """Does basic model work?"""

        u = self.u

        m = Message(
            user_id=self.uid,
            text='test content'
        )

        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "test content")

    def test_message_likes(self):
        """How does liking messages work"""

        m1 = Message(user_id=self.uid, text='test content')
        m2 = Message(user_id=self.uid, text='this is the way')

        u2 = User.signup("mando22", "mando@email.com", "password", None)
        u2id = 555
        u2.id = u2id
        db.session.add_all([m1, m2, u2])
        db.session.commit()

        u2.likes.append(m1)
        db.session.commit()

        likes = Likes.query.filter(Likes.user_id == u2id).all()
        self.assertEqual(len(likes), 1)
        self.assertEqual(likes[0].message_id, m1.id)