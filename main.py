from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///musical_broccoli.db"
db = SQLAlchemy(app)

class Url(db.Model):
    id = mapped_column(Integer, primary_key=True)
    original_url = mapped_column(String(500), nullable=False)
    shortened_url = mapped_column(String(20), unique=True, nullable=False)

@app.route('/')
def index():
    # TODO: Could add a UI for inputting a url to shorten, just a text field and
    # a button that makes a POST call to the /shortenUrl endpoint (might require
    # using Ajax to do the API call with the correct JSON format)
    return 'Welcome to URL Shortener!'

@app.route('/shortenUrl', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url', None)
    # TODO: Could add handling for creating custom short tokens
    # TODO: Should also add handling here for unsafe url types
        # such as data: or javascript:
    if long_url is None:
        # Bad request
        return jsonify({"error": "url is required"}), 400
    
    existing_url = Url.query.filter_by(original_url=long_url).first()
    if existing_url:
        # TODO: IF the user wants a new token, not the old one we currently don't
        # handle that (for example if they want to replace the old token with a
        # new custom token)
        return jsonify({"shortened_url": existing_url.shortened_url}), 200
        # shortened url already exists we can just return that
    
    # generate a new shortened url
    short_token = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    # TODO: Possibility for duplicate short tokens for different long URLs, would
    # need to check for uniqueness
    # Currently we will always just return the first result even if there's a
    # duplicate
    short_url = request.root_url + short_token
    url_entry = Url(original_url=long_url, shortened_url=short_url)
    db.session.add(url_entry)
    db.session.commit()
    return jsonify({"shortened_url": short_url}), 200

@app.route('/<short_token>', methods=['GET'])
def redirect_short_url(short_token):
    short_url = request.root_url + short_token
    url_entry = Url.query.filter_by(shortened_url=short_url).first()
    if url_entry is None:
        return jsonify({"error": "url not found"}), 404
    return redirect(url_entry.original_url)

@app.route('/getOriginalUrl', methods=['GET'])
def get_long_url():
    data = request.get_json()
    short_url = data.get('url')
    if not short_url:
        return jsonify({"error": "url is required"}), 400
    url_entry = Url.query.filter_by(shortened_url=short_url).first()
    if url_entry is None:
        return jsonify({"error": "url not found"}), 404
    return jsonify({"original_url" : url_entry.original_url}), 200


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)