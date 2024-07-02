import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Club model
class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shortbio = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(100), nullable=False)

    # Define relationships
    events = db.relationship('Event', backref='club', lazy=True)
    officers = db.relationship('Officer', backref='club', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)

class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)

@app.route('/')
def index():
    clubs = Club.query.all()
    return render_template('index.html', clubs=clubs)

@app.route('/club/<int:club_id>')
def one_club(club_id):
    club = Club.query.get_or_404(club_id)
    return render_template('club_page.html', club=club)

if __name__ == "__main__":
    app.run(debug=True)
