from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

db = "quotes_and_users"

class Quote:
    def __init__( self , data ):
        self.id = data['id']
        self.author = data['author']
        self.quote = data['quote']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.author_id = data['author_id']

        # self.users = []
        self.author_first_name = data['author_first_name']
        self.author_last_name = data['author_last_name']

        self.likes = 0

    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO quotes (author, quote, author_id)
        VALUES (%(author)s, %(quote)s, %(author_id)s);"""
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all_quotes_by_one_poster(cls, data):
        query = """
        SELECT * FROM quotes
        LEFT JOIN users ON users.id = quotes.author_id
        WHERE quotes.author_id = %(author_id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        all_quotes = []
        for quote in results:
            all_quotes.append(cls(quote))
        return all_quotes

    @classmethod
    def get_all_quotes(cls):
        query = """
        SELECT * FROM quotes
        LEFT JOIN users ON users.id = quotes.author_id;"""
        results = connectToMySQL(db).query_db(query)
        quotes = []
        for quote in results:
            quotes.append(cls(quote))
        return quotes

    @classmethod
    def get_all_likes(cls):
        query = """
        SELECT * FROM quotes
        JOIN likes ON quotes.id = likes.quote_id;"""
        results = connectToMySQL(db).query_db(query)
        quotes = []
        for quote in results:
            current_quote = {
                'id' : quote['id'],
                'author' : quote['author'],
                'quote' : quote['quote'],
                'created_at' : quote['created_at'],
                'updated_at' : quote['updated_at'],
                'author_id' : quote['author_id'],
                'author_first_name' : User.get_by_id({"id":quote['author_id']}).first_name,
                'author_last_name' : User.get_by_id({"id":quote['author_id']}).last_name
            }
            if len(quotes) == 0:
                quotes.append(cls(current_quote))
            else:
                last_quote = quotes[len(quotes)-1]
                if last_quote.id != current_quote['id']:
                    quotes.append(cls(current_quote))
            last_quote = quotes[len(quotes)-1]
            last_quote.likes+=1
        print(last_quote.likes)
        print("********")
        return quotes

    @classmethod
    def like(cls, data):
        query = """
        INSERT INTO likes (user_id, quote_id)
        VALUES (%(user_id)s, %(quote_id)s);"""
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = """
        DELETE FROM quotes
        WHERE id = %(id)s;"""
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_quote(quote):
        is_valid = True
        if len(quote['author']) < 3:
            is_valid = False
            flash("Author name must be at least 3 characters","quote")
        if len(quote['quote']) < 3:
            is_valid = False
            flash("Please enter a quote.","quote")
        return is_valid