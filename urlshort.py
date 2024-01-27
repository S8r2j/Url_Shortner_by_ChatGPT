from flask import render_template, request, redirect, Blueprint, jsonify, url_for
from db.model import db, Url, jwt, login_manager, User
from flask_login import login_required,login_user,logout_user, current_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import random
import string

router = Blueprint('urlshortener', __name__, template_folder='templates')

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


@router.route('/')
def index():
    return render_template('index.html')


@router.route('/shorten/', methods = ['POST'])
def shorten():
    original_url = request.form.get('url')
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'http://' + original_url

    url_entry = Url.query.filter_by(original_url = original_url).first()

    if url_entry:
        short_url = url_entry.short_url
    else:
        short_url = generate_short_url()
        new_url = Url(original_url = original_url, short_url = short_url)
        db.session.add(new_url)
        db.session.commit()

    host = request.host_url
    full_short_url = host + short_url
    return render_template('index.html', short_url = full_short_url)

@router.route('/short/url/', methods = ['POST'])
@login_required
def shorturl():
    original_url = request.form.get('url')
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'http://' + original_url

    url_entry = Url.query.filter_by(original_url = original_url).first()

    if url_entry:
        short_url = url_entry.short_url
    else:
        short_url = generate_short_url()
        new_url = Url(original_url = original_url, short_url = short_url)
        db.session.add(new_url)
        db.session.commit()

    host = request.host_url
    full_short_url = host + short_url
    return render_template('welcome.html', user_name= current_user.username, short_url = full_short_url)

@router.route('/<short_url>')
def redirect_to_original(short_url):
    url_entry = Url.query.filter_by(short_url = short_url).first()

    if url_entry:
        return redirect(url_entry.original_url)
    else:
        return 'URL not found', 404


@router.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')

        existing_user = User.query.filter_by(username = username).first()
        if existing_user:
            return 'Username already exists. Choose a different one.'

        new_user = User(username = username, password = password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('urlshortener.login'))

    return render_template('signup.html')

@router.route('/profile/', methods = ['GET', 'POST'])
@login_required
def profile():
    user = current_user
    return render_template('welcome.html', user_name = user.username)
@router.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('urlshortener.profile'))
        else:
            return 'Invalid login credentials.'

    return render_template('login.html')


@router.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('urlshortener.index'))


# JWT token generation endpoint
@router.route('/get_token', methods = ['POST'])
def get_token():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username = username).first()

    if user and user.password == password:
        access_token = create_access_token(identity = username)
        return jsonify(access_token = access_token)
    else:
        return 'Invalid login credentials.', 401


# Protected endpoint using JWT
@router.route('/protected', methods = ['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as = current_user), 200
