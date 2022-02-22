from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.quote import Quote

@app.route('/quote/destroy/<int:id>')
def destroy_quote(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Quote.destroy(data)
    return redirect('/dashboard')


