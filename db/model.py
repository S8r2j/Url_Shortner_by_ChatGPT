from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from core.config import setting

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{setting.DATABASE_USER}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOST}/{setting.DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the 'Url' model
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_url = db.Column(db.String(255), nullable=False)
    short_url = db.Column(db.String(20), nullable=False, unique=True)

with app.app_context():
    db.create_all()