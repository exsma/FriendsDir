
from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import db, User, Friend, Location, connect_to_db
import crud
from jinja2 import StrictUndefined
import json
from newsapi import NewsApiClient
from flask import Blueprint
import flask_paginate

# import newsget

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!


@app.route('/')
def homepage():
    """View homepage."""
    if 'email' in session:
        navbar='loggedin'
    else:
        navbar='logged out'

    return render_template('homepage.html',navbar=navbar )



@app.route('/createaccount')
def create_account():
    """View acount creating."""
    if 'email' in session:
        navbar='loggedin'
    else:
        navbar='logged out'
    return render_template('createaccount.html',navbar=navbar)


@app.route('/login')
def Login():
    """View acount creating."""
    if 'email' in session:
        navbar='loggedin'
    else:
        navbar='logged out'
    return render_template('login.html',navbar=navbar)


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
    if 'email' in session:
        navbar ='loggedin'
    else:
        navbar='logged out'

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
    user = crud.get_user_by_email(email)
    if 'email' in session:
        navbar='loggedin'
    else:
        navbar='logged out'
    if user:
        if password == crud.get_password_by_email(email):
            session['email']=email
            flash(f'Logged in as {email}')
            return redirect('/user-homepage')
        else:
            flash('Wrong password or username!')
            return redirect('/login')
    else:
        flash('Wrong password or username!')
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
    """handle add a friend page"""
    if 'email' in session:
        navbar='loggedin'
    else:
        navbar='logged out'

    if "email" in session:
        return render_template('add-a-friend.html', navbar=navbar)
    else:
        return render_template('login.html',navbar=navbar)

@app.route('/delete-a-friend<friend_id>', methods=['POST'])
def delete_a_friend_page(friend_id):
    """delete a friend."""
    if 'email' in session:
        navbar='loggedin'
    else:
        navbar='logged out'

    if "email" in session:
        friend=crud.get_friends_by_friend_id(friend_id)
        crud.delete_friend(friend)
        flash('Friend deleted')
        return redirect("user-homepage")
    else:
        return render_template('login.html',navbar=navbar)

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
    if 'email' in session:
        navbar='loggedin'
    else:
        navbar='logged out'

   # session['displaying'] = 

    if 'email' in session:
        page = request.args.get('page', 1, type=int)
        print('=================================')
        print(page)
       
        c_user_id = crud.get_user_by_email(session.get("email")).user_id
        paginate_list_friend= Friend.query.filter(Friend.user_id == c_user_id).paginate(page=page, per_page=3)
        
        list_friend= crud.get_user_by_email(session.get("email")).friends
        # list_friend_paginate= crud.get_user_by_email(session.get("email")).friends
        
        with open("cityMap.json") as c:
            continents = json.loads(c.read())
        print('===========================================')
        print (paginate_list_friend)
        return render_template("user-homepage.html",paginate_list_friend=paginate_list_friend, friends=list_friend, continents=continents, navbar=navbar)

    else:
        return redirect('/')


@app.route('/all-friends')
def all_friends():
    """View all your friends."""
    friends = crud.Friend.query.filter().all()
   
    # a_friend = crud.get_friends_by_friend_id(session['friend_id']).first()
    if 'email' in session:
        navbar='loggedin'
    else:
        navbar='logged out'
    if len(friends)>9:
        status="most"
    elif len(friends)>6:
        status="many"
    else:
        status="less"
    if "email" in session:
        return render_template('user-homepage.html', friends=friends,navbar=navbar, status=status)
    else:
        return render_template('login.html',navbar=navbar)


@app.route('/all-friends/<friend_id>')
def one_friend(friend_id):
    """View a friend"""
    a_friend = crud.get_friends_by_friend_id(friend_id)
    Country = a_friend.location.country
    if 'email' in session:
        navbar='loggedin'
    else:
        navbar='logged out'


    if Country == 'Syrian Arab Republic':
        Country = 'Syria'
    if Country == 'Turkey':
        Country = 'Istanbul'
    
    newsapi = NewsApiClient(api_key='924f7c4fba0948679273ceec6d5c666c')
    news_get_1 = newsapi.get_everything(q=Country, language='en')
    if "email" in session:
        # if session.get('email')== a_friend.user.user_id:
        return render_template('friend-profile.html',a_friend=a_friend, news_get_1=news_get_1, Country=Country, navbar=navbar)
        # else:
            # return redirect('user-hompage')
    else:
        return render_template('login.html',navbar=navbar)

        

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)