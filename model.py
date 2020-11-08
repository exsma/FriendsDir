from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    location = db.relationship('Location')

    # location = db.relationship('Location', backref='users')

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Friend(db.Model):
    """A friend to the user."""

    __tablename__ = 'friends'

    friend_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    dob = db.Column(db.DateTime)
    ffname = db.Column(db.String, nullable=False)
    flname = db.Column(db.String)
    friend_email = db.Column(db.String)
    friend_notes = db.Column(db.Text)
    friend_number = db.Column(db.String)
    portrait = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))


    user = db.relationship('User', backref='friends')
    location = db.relationship('Location', backref='friends')

    def __repr__(self):
        return f'<User friend_id={self.friend_id} ffname={self.ffname}>'

class Location(db.Model):
    """A geographical location."""

    __tablename__ = 'locations'

    location_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    country = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    city= db.Column(db.String, nullable=False)
    time_zone=db.Column(db.DateTime)
    

    def __repr__(self):
        return f'<location country={self.country}>'


def connect_to_db(flask_app, db_uri='postgresql:///friendzati', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)


# class Timezone(db.Model):
#     """A geographical location."""

#     __tablename__ = 'timezones'

#     location_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True
#                         nullable=False)
#     timestamp = db.Column(db.String, nullable=False)
#     state = db.Column(db.String, nullable=False)
#     city= db.Column(db.String, nullable=False)
#     time_zone=db.Column(db.String, )
    

#     def __repr__(self):
#         return f'<location country={self.country}>'
