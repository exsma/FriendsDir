
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



@app.route('/createaccount')
def create_account():
    """View acount creating."""

    return render_template('createaccount.html')


@app.route('/login')
def Login():
    """View acount creating."""

    return render_template('login.html')


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
        # user_location = crud.create_location(country="USA", city="MN", state="mn")
        my_location = crud.create_location(country, state, city)
        crud.create_user(email, password, fname, lname, my_location)
    

        return redirect('/login')


    
@app.route('/handle-login', methods=['POST'])
def handle_login():
    """Log user into application."""

    email = request.form['email']
    password = request.form['password']
    provided_password= crud.get_password_by_email(email)
    if password == provided_password:
        session['email']=email
        flash(f'Logged in as {email}')
        return redirect('/user-homepage')

    else:
        flash('Wrong password!')
        return redirect('/login')

@app.route("/handle-logout")
def handle_logout():
    """Log user out and say goodbye"""

    if "email" in session:
        del session["email"]
    
    flash("You have signed out")

    return redirect("/")

@app.route('/add-a-friend')
def add_a_friend_page():
    """View acount creating."""
    if "email" in session:
        return render_template('add-a-friend.html')
    else:
        return render_template('login.html')

@app.route('/add-a-friend-new', methods=['POST'])
def register_friend():
    if "email" in session:
        email = request.form['email']
        # dob =  datetime.strptime(request.form['dob'], '%Y-%m-%d') 
        ffname = request.form['fname']
        flname = request.form['lname']
        notes = request.form['notes']
        friend_number = request.form['Pnumber']
        portrait = request.form['portrait']
        country = request.form['country']
        city = request.form['city']
        state = request.form['state']
        # current_user_email = session['email']

        # user_location = crud.create_location(country="USA", city="MN", state="mn")
        friend_location = crud.create_location(country, state, city)
        friends_user = crud.get_user_by_email(session.get('email'))
        crud.create_friend(ffname, flname, friend_location, email, friend_number, notes, portrait, friends_user)
        flash('Friend Added')
        return redirect('/user-homepage')

@app.route("/user-homepage")
def friends_list():
    """Return page showing the users friends"""
    list_friend= crud.get_user_by_email(session.get("email")).friends
    
    if 'email' in session:
        return render_template("user-homepage.html", friends=list_friend)

    else:
        return render_template("homepage.html")


@app.route('/all-friends')
def all_friends():
    """View all your friends."""
    # session["friend_id"] = crud.Friend.friend_id
    friends = crud.Friend.query.filter().all()
    # a_friend = crud.get_friends_by_friend_id(session['friend_id']).first()
    if "email" in session:
        return render_template('user-homepage.html', friends=friends)
    else:
        return render_template('login.html')


@app.route('/all-friends/<friend_id>')
def one_friend(friend_id):
    """View a friend"""
    a_friend = crud.get_friends_by_friend_id(friend_id)
    
    if "email" in session:
        return render_template('friend-profile.html',a_friend=a_friend)
    else:
        return render_template('login.html')

        



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)