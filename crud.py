from model import db, User, Friend, Location, connect_to_db


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


def create_user(email, password, fname, lname, location):
    """Create and return a new user."""

    user = User(email=email, 
                password=password, 
                fname=fname,   
                lname=lname,
                location=location)

    db.session.add(user)
    db.session.commit()

    return user

   

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_email_paginate(email):
    """Return a user by email."""

    return User.query.filter(User.email == email)

def get_password_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first().password

def create_friend(ffname, flname, location, friend_email, friend_number, friend_notes, portrait, user):
    """Create and return a new friend."""

    friend = Friend(ffname=ffname,
                    flname=flname,
                    location=location,
                    friend_email=friend_email,
                    friend_number=friend_number,
                    friend_notes=friend_notes,
                    portrait=portrait,
                    user=user)

    db.session.add(friend)
    db.session.commit()

    return friend

# def get_friends_by_user():
#     """Return all friends."""

#     return Friend.query.filter(User.user_id == Friend.user_id).all()

def get_friends_by_friend_id(friend_id):
    """Return all friends."""

    return Friend.query.filter(Friend.friend_id == friend_id).first()


def delete_friend(friend):
    """delete a friend"""
    db.session.delete(friend.location)
    db.session.delete(friend)
    db.session.commit()


def create_location(country, state, city):
    """a location."""

    location = Location(country=country, 
                state= state, 
                city=city
                )

    db.session.add(location)
    db.session.commit()

    return location
    
