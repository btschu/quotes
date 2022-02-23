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
        self.user_id = data['user_id']

        self.users = []

        self.likes = 0

    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO quotes (author, quote, user_id)
        VALUES (%(author)s, %(quote)s, %(user_id)s);"""
        return connectToMySQL(db).query_db(query,data)

    # @classmethod
    # def get_all_users_that_post_quotes(cls,data):
    #     query = """
    #     SELECT * FROM quotes
    #     JOIN users ON users.id = quotes.user_id;"""
    #     results = connectToMySQL(db).query_db(query, data)
    #     users = cls(results[0])
    #     for row in results:
    #         user_data = {
    #             'id' : row[users.id],
    #             'first_name' : row[users.first_name],
    #             'last_name' : row[users.last_name]
    #         }
    #         users.quotes.append(User(user_data))
    #     return users

    @classmethod
    def get_all_quotes_by_one_poster(cls, data):
        query = """
        SELECT * FROM quotes
        LEFT JOIN users ON users.id = quotes.user_id
        WHERE quotes.user_id = %(user_id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        all_quotes = []
        for quote in results:
            all_quotes.append(cls(quote))
        return all_quotes

    @classmethod
    def get_all_likes(cls):
        query = """
        SELECT * FROM quotes
        JOIN users ON users.id = quotes.user_id
        LEFT JOIN likes ON quotes.id = likes.quote_id;"""
        results = connectToMySQL(db).query_db(query)
        quotes = []
        for quote in results:
            current_quote = {
                'id' : quote['id'],
                'author' : quote['author'],
                'quote' : quote['quote'],
                'created_at' : quote['users.created_at'],
                'updated_at' : quote['users.updated_at'],
                'user_id' : quote['user_id'],
                'first_name' : quote['first_name'],
                'last_name' : quote['last_name']
            }
            if len(quotes) == 0:
                quotes.append(cls(current_quote))
            else:
                last_quote = quotes[len(quotes)-1]
                if last_quote.id != current_quote['id']:
                    quotes.append(cls(current_quote))
            last_quote = quotes[len(quotes)-1]
            last_quote.likes+=1
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