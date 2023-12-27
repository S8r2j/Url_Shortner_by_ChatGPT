from flask import render_template, request, redirect, Blueprint
from db.model import db, Url
import sqlite3
import random
import string

router = Blueprint('urlshortener', __name__, template_folder='templates')



# Function to generate a random short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


# Routes
@router.route('/')
def index():
    return render_template('index.html')


@router.route('/shorten', methods = ['POST'])
def shorten():
    original_url = request.form.get('url')

    # Check if the URL is valid (you can add more validation)
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'http://' + original_url

    # Check if the URL is already in the database
    result = Url.query.filter(Url.original_url == original_url).first()

    if result:
        short_url = result.short_url
    else:
        short_url = generate_short_url()
        data_insert = Url(original_url = original_url, short_url = short_url)
        db.session.add(data_insert)
        db.session.commit()
        db.session.refresh(data_insert)

    return render_template('index.html', short_url = request.host_url + short_url)


@router.route('/<short_url>')
def redirect_to_original(short_url):
    result = Url.query.filter(Url.short_url == short_url).first()
    if result:
        return redirect(result.original_url)
    else:
        return 'URL not found', 404
