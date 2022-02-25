from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.quote import Quote

# Create new quote

@app.route('/quote/create',methods=['POST'])
def create_quote():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Quote.validate_quote(request.form):
        return redirect('/dashboard')
    data = {
        "author": request.form["author"],
        "quote": request.form["quote"],
        "user_id": session["user_id"]
    }
    Quote.save_quote(data)
    return redirect('/dashboard')

# View all quotes by one poster

@app.route('/quote/<int:user_id>')
def all_quotes_posted_by_one_author(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id":user_id,
    }
    user_data = {
        "id":session['user_id']
    }
    context = {
        "quotes" : Quote.get_all_quotes_by_one_poster(data),
        "user" : User.get_by_id(user_data),
    }
    return render_template("user_quote.html", **context)

# Add like to a quote

@app.route('/like_quote/<int:quote_id>')
def increase_like(quote_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'quote_id' : quote_id,
        'user_id' : session['user_id'],
    }
    Quote.like_quote(data)
    return redirect('/dashboard')