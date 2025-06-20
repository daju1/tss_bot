from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])



class DB_Session:
    def __init__(self):
        self.users = dict()

    def add_user(self, user):
        self.users[user.email] = user

    def test_user(self, user, password):
        msg = ""
        if user.email in self.users:
            if self.users[user.email].verify_password(password):
                msg +='Logged in successfully.'
                return (msg, True, user)
            msg += "user's password incorrect"
            print (msg)
        msg += "user.email not in users"
        print (msg)
        print (user.email)
        print (self.users)
        return (msg, False, user)

    def get_user(self, name):
        # try email
        if name in self.users:
            email = name
            user = self.users[email]
            return user

        for user in users:
            if user.username == name:
                return user


        return None

db_session = DB_Session()

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])


    def validate_on_submit(self):
        from .app import User
        user = User(self.username.data, self.email.data,
                    self.password.data)
        return db_session.test_user(user, self.password.data)

