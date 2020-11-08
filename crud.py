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

def create_friend(ffname, flname, dob, location, email, number, notes, portrait, user):
    """Create and return a new friend."""

    friend = Friend(ffname=ffname,
                    flname=flname,
                    dob=dob,
                    location=location,
                    email=email,
                    number=number,
                    notes=notes,
                    portrait=portrait,
                    user=user)

    db.session.add(friend)
    db.session.commit()

    return friend

def get_friends():
    """Return all friends."""

    return Friend.query.all()


def create_location(country, state, city):
    """a location."""

    location = Location(country=country, 
                state= state, 
                city=city
                )

    db.session.add(location)
    db.session.commit()

    return location
    
