#!/usr/local/bin/python
# coding: utf8

'''

pip3 install -r requirements.txt

or

pip3 install pandas
pip3 install Flask
pip3 install flask-login
pip3 install flask-WTF
pip3 install flask-httpauth
pip3 install passlib


start server
$ export FLASK_ENV=development
$ export FLASK_DEBUG=1
$ FLASK_APP=app.py flask run

test it by
http://127.0.0.1:5000/actualstock?


TODO: see
https://github.com/pallets/flask/tree/master/examples/tutorial
and you can take login, logout and register logic from there

now we have very primitive login and logout logic
http://127.0.0.1:5000/account/login
http://127.0.0.1:5000/account/logout

'''

import os

from flask import Flask

#from flask import Flask, session, redirect, url_for, request, flash
#from flask import jsonify, send_from_directory, render_template
from flask_login import LoginManager

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()



app = Flask(__name__, template_folder="./static")


login_manager = LoginManager()
login_manager.init_app(app)

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (URLSafeTimedSerializer
                          as Serializer, BadSignature, SignatureExpired)

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hash_password(password)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.email })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

print("app starts")

from mydblib import common

@app.route('/')
# @auth.login_required
def index():
    return common.get_tss_msg()

#@app.route('/')
#@auth.login_required
#def index():
    # if 'username' in session:
    #     return 'Logged in as %s' % escape(session['username'])
    # return 'You are not logged in'
#    return app.send_static_file('index.html')

@app.route('/test_auth')
@auth.login_required
def test_auth():
    return "Hello, %s!" % auth.username()

@app.route('/test')
@auth.login_required
def test():
    return app.send_static_file('test.html')


@app.route('/test_register', methods=['GET', 'POST'])
def register():
    # http://flask.pocoo.org/docs/1.0/patterns/wtforms/
    from .register import RegistrationForm
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        from .register import db_session
        db_session.add_user(user)
        flash('Thanks for registering')
        return redirect(url_for('test_login'))
    return render_template('test_register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/account/login_old', methods=['GET', 'POST'])
def login_old():
    # TODO
    # https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name="username">
            <p><input type=text name="password">
            <p><input type=submit value=Login>
        </form>
    '''



@app.route('/account/logout_old')
def logout_old():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

#@auth.get_password
def get_password(username):
    from .register import db_session
    user = db_session.get_user(username)
    if None == user:
        return None
    return user.password_hash

users = {
    "admin": "admin",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/test_login', methods=['GET', 'POST'])
def test_login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    from .register import LoginForm
    form = LoginForm(request.form)
    if request.method == 'POST':
        (msg, res, user) = form.validate_on_submit()
        if res:
            # Login and validate the user.
            # user should be an instance of your `User` class
            token = user.generate_auth_token()
            print("token", token)
            #login_user(user)

            flash('Logged in successfully.')

            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            #if not is_safe_url(next):
            #    return flask.abort(400)

            return redirect(next or url_for('test'))
            return redirect(next or url_for('index'))
        else:
            return render_template('test_login.html', form=form, msg=msg)

    return render_template('test_login.html', form=form)



@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username







@app.route('/static/<path:path>')
@auth.login_required
def send_static(path):
    return send_from_directory('./static', path)

@app.route('/post/<int:post_id>')
@auth.login_required
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/get/<int:get_id>')
@auth.login_required
def show_get(get_id):
    # show the get with the given id, the id is an integer
    return 'Get %d' % get_id

@app.route('/path/<path:subpath>')
@auth.login_required
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
