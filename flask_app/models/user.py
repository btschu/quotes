from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = "quotes_and_users"

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.quotes = []

    @classmethod
    def save(cls,data):
        query = """INSERT INTO users (first_name, last_name, email, password)
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"""
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;"""
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;"""
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
        UPDATE users
        SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s
        WHERE id = %(id)s;"""
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_edit_user(user):
        is_valid = True
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;"""
        connectToMySQL(db).query_db(query,user)
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","login")
            is_valid=False
        return is_valid

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;"""
        results = connectToMySQL(db).query_db(query,user)
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","login")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid = False
        if not any(char.isdigit() for char in user['password']):
            flash("Password should have at least one number", "register")
            is_valid = False
        if not any(char.isupper() for char in user['password']):
            flash("Password should have at least one uppercase letter", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid