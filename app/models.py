from datetime import datetime
from hashlib import md5
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt
<<<<<<< HEAD
from app import db, login
from app.search import add_to_index, remove_from_index, query_index





class SearchableMixin(object):
    '''
    Mixin class attached to model for automatic management of full-text search.
    
    The self argument that is used in regular instance mehtods is renamed to cls,
    to highlight that the method receives a class and not an instance as its first
    argument.
    '''

    @classmethod
    def search(cls, expression, page, per_page):
        '''
        Class method to wrap the query_index() function from app/search.py 
        to replace the list of object IDs with actual objects. 
        '''

        # function to return the list of ids and the total number of results
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total


    @classmethod
    def before_commit(cls, session):
        '''
        Before handler to figure out what objects are going to be added, modified or deleted.
        '''

        session._changes = {
            'add':list(session.new),
            'update':list(session.dirty),
            'delete':list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        '''
        Iterate over the added, modified and deleted objects 
        and make the corresponding calls to the indexing functions for the objects that have the SearchableMixin class.
        '''

        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)   
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj, __tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):   
                remove_from_index(obj.__tablename__, obj)
        session._changes = None


    @classmethod
    def reindex(cls):
        '''
        Helper method to refresh an index what all relational data.
        '''
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


# Set up event handles that will make SQLAlchemy call the before_commit() and after_commit() methods before and after each commit.
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
=======
from app import app
>>>>>>> parent of aaa9c08... Restructured application by seperate subsytems

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


    def get_reset_password_token(self, expires_in=600):
        '''
        Generates a JWT token as a string
        '''
        # utf-8 neccessary as jswt.encode() returns function as a byte sequence
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm = 'HS256').decode('utf-8')


    @staticmethod
    def verify_reset_password_token(token):
        '''
        Static method which takes a token and attempts to decode it.
        '''
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
            algorithms=['HS256'])['reset_password']

        # if token can not be decoded and exception is raised and None is returned to caller
        except:
            return
        
        # if token valid then user is loaded and reset_password key is the id of the user
        return User.query.get(id)



@login.user_loader
def load_user(id):
    '''
    Loader function to keep track of logged in user by storing its user id in session
    '''
    return User.query.get(int(id))


<<<<<<< HEAD
class Post(SearchableMixin, db.Model):

    
    # class attribute that lists the fields to be included in the index
    # set the body field to be indexed
    __searchable__ = ['body']
    
=======
class Post(db.Model):
    '''
    Class to represent User posts
    '''
>>>>>>> parent of aaa9c08... Restructured application by seperate subsytems

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # indexed for retrieving posts in chronological order - lookup
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # INCONSISTENCY with class call - User normally starts with uppercase letter but SQLAlchemy automatically uses lowercase letters
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

<<<<<<< HEAD








=======
>>>>>>> parent of aaa9c08... Restructured application by seperate subsytems
