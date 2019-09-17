from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post


# before-request decorator executes function right before any view
@app.before_request
def before_request():
    '''
    Record time of last visit
    '''
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    # check form validation
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        # redirect used to mitigate possible annoyance with how the refresh command is implemented in browser
        return redirect(url_for('index'))
    # test posts
    # posts =[
    #     {
    #         'author':{'username':'John'},
    #         'body': 'beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    #returns all posts of followed users
    posts = current_user.followed_posts().all()
    return render_template('index.html', title='Home Page', form=form, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    User login function
    '''
    # do not allow logged in users to navigate to log in page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # create new instance of LoginForm class    
    form = LoginForm()
    # if form is validated then search for user
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # if no user found or password is incorrect redirect
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # log user in
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        
        
        # 3 possible cases to redirect after a successful login
            
        #    1) If the login URL does not have a next argument, then the user is redirected to the index page
        #    2) If the login URL includes a next argument that is set to a relative path (or in other words, a URL without the domain portion), then the user is redirected to that URL
        #    3) If the login URL includes a next argument that is set to a full URL that includes a domain name, then the user is redirected to the index page

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    '''
    User logout function
    '''
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    User register function
    '''
    # check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# app route with dynamic component for username
@app.route('/user/<username>')
@login_required
def user(username):
    '''
    User profile page
    '''
    # return first user or 404 page
    user = User.query.filter_by(username=username).first_or_404()

    # test posts
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    '''
    Editing user profile
    '''
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        # copy form data to current user object
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        # write object to db
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    # if GET method then provide form with fields populated from user
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {} anymore.'.format(username))
    return redirect(url_for('user', username=username))



