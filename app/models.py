from datetime import datetime
from hashlib import md5
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# followers association table - Followers not declared as model as it is an auxiliary table
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# Create model for User database table
class User(UserMixin, db.Model):
    '''
    User class contains variables relating to user

    Class inherits from db.Model - the base class for all models in SQLAlchemy

    All fields are created as instances of db.Column class
    '''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    # last seen time
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User', secondary=followers, 
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref('followers',lazy='dynamic'), lazy='dynamic'
        )

    # Instruction of how to print objects of the class
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        '''
        Set password and generate password hash
        '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''
        Check that password matches generated password hash
        '''
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        '''
        Return URL of user's avatar image and scale to requested size
        '''
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # add and remove relationships between user accounts

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        '''
        Query to check if a link between two users already exists
        '''
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        ''' 
        Return a list of followed posts for user on index page
        '''
        followed= Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        # return own User posts
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())



@login.user_loader
def load_user(id):
    '''
    Loader function to keep track of logged in user by storing its user id in session
    '''
    return User.query.get(int(id))


class Post(db.Model):
    '''
    Class to represent User posts
    '''

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # indexed for retrieving posts in chronological order - lookup
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # INCONSISTENCY with class call - User normally starts with uppercase letter but SQLAlchemy automatically uses lowercase letters
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

