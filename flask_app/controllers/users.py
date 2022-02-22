from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.quote import Quote
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Login to site

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def user_login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

# Create new user

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/registration')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

# Dashboard

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
    }
    context = {
        # "likes":Quote.get_all_likes(data),
        "user" : User.get_by_id(data),
        "quotes" : Quote.get_all_likes()
    }
    return render_template("dashboard.html", **context)

@app.route('/quote/create',methods=['POST'])
def create_quote():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Quote.validate_quote(request.form):
        return redirect('/dashboard')
    data = {
        "author": request.form["author"],
        "quote": request.form["quote"],
        "author_id": session["user_id"]
    }
    Quote.save(data)
    return redirect('/dashboard')

# Logout

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/account/edit/<int:id>')
def edit_account(id):
    if 'user_id' not in session:
        return redirect('/logout')
    # data = {
    #     "id":id
    # }
    user_data = {
        "id":session['user_id']
    }
    context = {
        # "quotes" : Quote.get_all_quotes(),
        "edit" : User.get_by_id(user_data),
        # "user" : User.get_by_id(user_data)
    }
    return render_template("edit_account.html", **context)

@app.route('/account/update',methods=['POST'])
def update_account():
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = request.form['id']
    if not User.validate_edit_user(request.form):
        return redirect(f'/account/edit/{user_id}')
    data = {
        "id": session["user_id"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }
    User.update(data)
    return redirect('/dashboard')

@app.route('/quote/<int:author_id>')
def all_quotes_posted_by_one_author(author_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "author_id":author_id,
        'author_first_name' : Quote.get_all_quotes_by_one_poster({"author_id":author_id}).first_name,
        'author_last_name' : Quote.get_all_quotes_by_one_poster({"author_id":author_id}).last_name
    }
    user_data = {
        "id":session['user_id']
    }
    context = {
        "quotes" : Quote.get_all_quotes_by_one_poster(data),
        "user" : User.get_by_id(user_data),
    }
    return render_template("user_quote.html", **context)

@app.route('/like_quote/<int:quote_id>')
def increase_like(quote_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'quote_id' : quote_id,
        'user_id' : session['user_id'],
    }
    Quote.like(data)
    return redirect('/dashboard')