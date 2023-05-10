"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

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


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        # Create some users to use in the tests
        self.u = User(email="test@test.com",username="testuser",password="HASHED_PASSWORD")
        self.u1 = User(email="test1@test.com",username="testuser1",password="HASHED_PASSWORD1")
        self.u2 = User(email="test2@test.com",username="testuser2",password="HASHED_PASSWORD2")

        db.session.add_all([self.u, self.u1, self.u2])
        db.session.commit()

    def tearDown(self):
        """Remove all created test data."""

        db.session.rollback()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""

        # u = User(email="test@test.com", username="testuser", password="HASHED_PASSWORD")
        # db.session.add(u)
        # db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(self.u.messages), 0)
        self.assertEqual(len(self.u.followers), 0)

    def test_repr(self):
        """Does the repr method work as expected?"""
        self.assertEqual(repr(self.u), f"<User #{self.u.id}: {self.u.username}, {self.u.email}>")

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""

        # Test when user1 is following user2
        self.u1.following.append(self.u2)
        db.session.commit()
        self.assertTrue(self.u1.is_following(self.u2))

    def test_is_not_following(self):
        """Does is_following successfully detect when user1 is not following user2?"""

        # Test when user1 is not following user2
        self.assertFalse(self.u1.is_following(self.u2))

    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""

        # Test when user1 is followed by user2
        self.u1.followers.append(self.u2)
        db.session.commit()
        self.assertTrue(self.u1.is_followed_by(self.u2))

    def test_is_not_followed_by(self):
        """Does is_followed_by successfully detect when user1 is not followed by user2?"""

        # Test when user1 is not followed by user2
        self.assertFalse(self.u1.is_followed_by(self.u2))

    def test_create_user(self):
        """Does User.create successfully create a new user given valid credentials?"""

        # Test creating a new user with valid credentials
        new_user = User.signup(
            username="newuser",
            email="newuser@test.com",
            password="HASHED_PASSWORD3",
            image_url="/static/images/default-pic.png"
        )
        db.session.commit()
        self.assertEqual(new_user.username, "newuser")

    def test_create_user_fail(self):
        """Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""

        # Test failing to create a new user with invalid credentials (username AND/OR email already exists)
        new_user = User.signup(
            username="testuser",
            email="test44@test.com",
            password="HASHED_PASSWORD4",
            image_url="/static/images/default-pic.png"
        )
        db.session.commit()
        self.assertIsNone(new_user)
        #db.session.rollback()
