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
    shortened_url = mapped_column(String(10), unique=True, nullable=False)

@app.route('/shortenUrl', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url', None)
    print("Request Data: ", data)
    if long_url is None:
        # Bad request
        return jsonify({"error": "url is required"}), 400
    
    existing_url = Url.query.filter_by(original_url=long_url).first()
    if existing_url:
        return jsonify({"short_url": existing_url.shortened_url})
        # shortened url already exists we can just return that
    
    # generate a new shortened url
    short_end = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    short_url = request.root_url + short_end
    print(short_url)
    url_entry = Url(original_url=long_url, shortened_url=short_end)
    db.session.add(url_entry)
    db.session.commit()

    return jsonify({"shortened_url": short_url})

@app.route('/<short_url>', methods=['GET'])
def redirect_short_url(short_url):
    
    url_entry = Url.query.filter_by(shortened_url=short_url).first()
    if url_entry is None:
        return jsonify({"error": "url not found"}), 404
    return redirect(url_entry.original_url)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)