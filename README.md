# Warbler

A twitter clone.. of sorts. Built with Flask, SQLAlchemy, Postgres & Bootstrap

# **Further Study**

There are lots of areas of further study.

You won’t have time to do all of these. Instead, pick those that seem most interesting to you.

### **[x] Make like button only appear on messages that aren't yours**

This one was pretty straightforward

### **[ ] Custom 404 Page**

Learn how to add a custom 404 page, and make one.

### **[ ] Add AJAX**

There are two areas where AJAX would really benefit this site:

-   When you like/unlike a warble, you shouldn’t have to refresh the page
-   You should be able to compose a warble via a popup modal that is available on every page via the navigation bar button.

### **[ ] DRY Up the Templates**

There’s a lot of repetition in this app!

Here are some ideas to clean up repetition:

-   Learn about the `{% include %}` statement in Jinja and use this to not have the forms be so repetitive.
-   Learn about the `{% macro %}` and `{% import %}` statements in Jinja; you can use these to be even more clever, and get rid of a lot of repetition in the user detail, followers, followed_user pages, and more.

### **[ ] DRY Up the Authorization**

**Advanced but interesting**

In many routes, there are a few lines that check for is-a-user-logged-in. You could solve this by writing your own “decorator”, like “@app.route”, but that checks if the **_g.user_** object is not null and, if not, flashes and redirects.

You’ll need to do some searching and reading about Python decorators to do this.

### **[ ] DRY Up the URLs**

Throughout the app, there are many, many places where URLs for the app are hardcoded throughout – consider the number of places that refer to URLs like **_/users/[user-id]_**.

Flask has a nice feature, **_url_for()_**, which can produce the correct URL when given a view function name. This allows you to not use the URLs directly in other routes/templates, and makes it easier in the future if you even needed to move URLs around (say, is **_/users/[user-id]_** needed to change to **_/users/detail/[user-id]_**.

Learn about this feature and use it throughout the site.

### **[ ] Optimize Queries**

In some places, Warbler may be making far more queries than it needs: the homepage can use more than 75 queries!

Using the Flask-DebugToolbar, audit query usage and fix some of the worst offenders.

### **[ ] Make a Change Password Form**

Make a form with three fields:

-   current password
-   new password
-   new password again, for confirmation

If the user is logged in *and* they provide the right password *and* their new passwords match, change their password.

Hint: do this by making a new method on the **_User_** class, rather than hard-coding stuff about password hashing in the view function.

### **[ ] Allow “Private” Accounts**

Add a feature that allows a user to make their account “private”. A private account should normally only the profile page without messages.

You can follow a private account — but that user will need to approve your follow. At the point you are successfully following a private account, you should then be able to see their messages.

**Note:** this will require some schema changes and thoughtful design. Can you do this in a way that doesn’t sprinkle (even more) if conditions around? Can you add any useful functions on the **_User_** or **_Message_** classes?

### **[ ] Add Admin Users**

Add a feature for “admin users” — these are users that have a new field on their model set to true.

Admin users can:

-   delete any user’s messages
-   delete any user
-   edit a user profile; when an admin user edits a profile, they should be able to see and set the “admin” field to make another user an admin

### **[ ] User Blocking**

Add a feature where users can block other users:

-   when viewing a user page, there should be a block/unblock button
-   blocked users view the blocker in any way

### **[ ] Direct Messages**

Add a feature of “direct messages” — users being able to send private messages to another user, visible only to that user.

There are lots of possibilities on how far you want to take this one.
