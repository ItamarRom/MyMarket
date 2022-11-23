from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, ItemForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Item
from werkzeug.urls import url_parse
from datetime import datetime, timedelta

# This decorator handles functions we want to run before each view function
@app.before_request
def before_request():
   if current_user.is_authenticated:
       current_user.last_seen = datetime.utcnow()
       db.session.commit()


# The route decorator is used to associate between the url argument and the function
@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template('index.html', title='Home')


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    items = Item.query.filter_by(user_id=user.id)
    return render_template('user.html', items=items,title=user.username, user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # First checking if the current user is logged in and if true
    # redirecting the user to the home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Creating an instance of the LoginForm class we defined in 'forms.py'
    form = LoginForm()
    # The if statement is FLase by default
    # The value is changed to True when the user submits a form with the POST request
    # and after checking all the submitted data is valid
    # If its false we jump directly to the return statement at the end
    if form.validate_on_submit():
        # Finding the user in the DB by its email from the form submission
        # The query will only return the object with the matching email
        user = User.query.filter_by(email=form.email.data.lower()).first()
        # If the query returned None or the passwords did not match
        # (The password check is performed using the check_password method
        # we defined in the User model)
        # then we flash an error and redirect back to the login page again
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', category='error')
            return redirect(url_for('login'))
        # After checking for correct username and password we log in the user
        # using the login_user function from Flask_login
        login_user(user, remember=form.remember_me.data)
        # getting the query string of a get request of the login page
        # after a get request for a login required page before logging in
        next_page = request.args.get('next')
        ###################################################
        # netloc:
        # Contains the Network-Location in the URL
        # which includes the domain itself and sometimes additional information and creds
        ###################################################
        # If there is no argument for a next page in the login URL
        # or the argument is set to a full URL that includes a domain name
        # (Checking if the netloc is not an empty string)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # If the argument exists and is set to a relative path
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # If a form is submitted and the data is valid we create a new user:
        # username and email attributes are taken from the form
        # password attribute is taken from the form and passed as an argument
        # to the set_password function defined in the User class
        # Then we add the user to the DB and commit the changes
        user = User(username=form.username.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!', category='success')
        return redirect(url_for('login'))

    return render_template('register.html', title='register', form=form)


@app.route('/market', methods=['GET','POST'])
@login_required
def market():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, price=form.price.data,user_id=current_user.id, owner=current_user)
        db.session.add(item)
        db.session.commit()
        flash('You have entered an item to the Marketplace!', category="success")
        return redirect(url_for('market'))

    # getting the argument 'q' from the request of the search form defined inside market.html
    # the value of q is set to the search query entered by the user
    q = request.args.get('q')
    # If q exists
    if q:
        item = Item.query.filter(Item.name.contains(q))
    else:
     # Will return all the items inside the DB , ordered by their id in an ascending order
        item = Item.query.order_by(Item.id).all()
    return render_template('market.html', title='Marketplace',form=form, items=item)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    q = request.args.get('q')
    if q:
        item = Item.query.filter(Item.name.contains(q))
    else:
        item = ''

    return render_template('search.html', title='Search', items=item)


@app.route('/item/delete/<item_id>')
@login_required
def delete_item(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('market'))