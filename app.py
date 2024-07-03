import os
from flask import Flask, render_template, request, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Event and Officer models first
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    club_name = db.Column(db.String(100), db.ForeignKey('club.name'), nullable=False)

    # Define a relationship to the Club model
    club = db.relationship('Club', backref=db.backref('events', lazy=True))

class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    club_name = db.Column(db.String(100), db.ForeignKey('club.name'), nullable=False)

    # Define a relationship to the Club model
    club = db.relationship('Club', backref=db.backref('officers', lazy=True))

# Now define the Club model after Event and Officer
class Club(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    shortbio = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    instagram = db.Column(db.String(100), nullable=True)
    youtube = db.Column(db.String(100), nullable=True)
    linkedin = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    facebook = db.Column(db.String(100), nullable=True)
    twitter = db.Column(db.String(100), nullable=True)

    # Define relationships with unique backref names
    club_events = db.relationship('Event', backref='event_club', lazy=True)
    club_officers = db.relationship('Officer', backref='officer_club', lazy=True)

@app.route('/')
def index():
    clubs = Club.query.all()
    return render_template('index.html', clubs=clubs)

@app.route('/club/<string:club_name>')
def one_club(club_name):
    club = Club.query.filter_by(name=club_name).first()
    if not club:
        abort(404)
    return render_template('club_page.html', club=club)

if __name__ == "__main__":
    app.run(debug=True)
