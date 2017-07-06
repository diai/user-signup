from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

@app.route("/")
def index():
     template = jinja_env.get_template('signup.html')
     return template.render()

@app.route("/welcome")
def welcome():
    username = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(username=username)

def validate_email(email):
    if email.count('@') == 1 and email.count('.') == 1 and ' ' not in email and len(email) >= 3 and len(email) <= 20:
        return True
    else:
        return False

@app.route('/validate-signup', methods=['POST'])
def validate_signup():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''

    if username == '' or password == '' or verify_password == '':
        username_error = 'Please enter a username'
        password_error = 'Please enter a password'
        verify_password_error = 'Please re-enter the password' 

    elif ' ' in username or ' ' in password or len(username) < 3 or len(username) > 20 or len(password) < 3 or len(password) > 20:
        username_error = 'Please enter a valid username without spaces and between 3 and 20 characters'
        password_error = 'Please enter a valid password without spaces and between 3 and 20 characters'
        verify_password_error = 'Please enter a valid password without spaces and between 3 and 20 characters'

    elif password != verify_password:
        password_error = 'Passwords do not match'
        verify_password_error = 'Passwords do not match'

    elif email != '' and not validate_email(email):
        email_error = 'Please enter a valid email between 3 and 20 characters'

    if username_error == '' and password_error == '' and verify_password_error == '' and email_error == '':
        return redirect('/welcome?username={0}'.format(username))
    else:
        template = jinja_env.get_template('signup.html')
        return template.render(username=username,
            email=email,
            username_error = username_error,
            password_error = password_error,
            verify_password_error = verify_password_error,
            email_error = email_error)

app.run()