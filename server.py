
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')



@app.route('/create-acount')
def login_form():
    """View acount creating."""

    return render_template('createacount.html')


@app.route('/login-form')
def acount_creating():
    """View acount creating."""

    return render_template('login-form.html')


@app.route('/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    country = request.form['country']
    city = request.form['city']
    state = request.form['state']

    user = crud.get_user_by_email(email)
    if user:
        return 'A user already exists with that email.'
    else:
        user_location = crud.create_location(country="USA", city="MN", state="mn")
        crud.create_user(email, password, fname, lname, user_location)

        return redirect('/login-form')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)