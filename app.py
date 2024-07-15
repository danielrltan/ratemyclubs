from flask import Flask, render_template, request, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import for Migrations
from flask_migrate import Migrate, migrate

# Settings for migrations
migrate = Migrate(app, db)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)

    # Define a relationship to the Club model
    # club = db.relationship('Club', backref=db.backref('events', lazy=True))

class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)

    # Define a relationship to the Club model
    # club = db.relationship('Club', backref=db.backref('officers', lazy=True))

# Now define the Club model after Event and Officer
class Club(db.Model):
    id = db.Column(db.String(100), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profilepicture = db.Column(db.String(100), nullable=True)
    websitekey = db.Column(db.String(100), nullable=False)
    shortname = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    contact = db.Column(db.String(100), nullable=True)
    instagram = db.Column(db.String(100), nullable=True)
    youtube = db.Column(db.String(100), nullable=True)
    linkedin = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    facebook = db.Column(db.String(100), nullable=True)
    twitter = db.Column(db.String(100), nullable=True)
    

class ClubCategoryRelation(db.Model):
    clubid = db.Column(db.String(100), nullable=False, primary_key=True)
    categoryname = db.Column(db.String(100), nullable=False, primary_key=True)

import json
import requests

scrapebp = Blueprint('scrape', __name__)

@scrapebp.cli.command('clubs')
def scrape():
    clubs_url = "https://westernu.campuslabs.ca/engage/api/discovery/search/organizations?top=400"
    resp_json = requests.get(clubs_url).json()

    clublist = resp_json["value"]

    for clubResponse in clublist:
        print(clubResponse["Id"])
        cur_club = Club(**{k.lower():v for k, v in clubResponse.items() if k in {'Id', 'Name', 'ProfilePicture', 'Summary', 'WebsiteKey', 'ShortName', 'Description'}})
        existingrow = db.session.query(Club).where(Club.id == cur_club.id)
        if existingrow.first() is None:
            db.session.add(cur_club)
        else:
            for k, v in clubResponse.items(): 
                if k in {'Id', 'Name', 'ProfilePicture', 'Summary', 'WebsiteKey', 'ShortName', 'Description'}:
                    setattr(existingrow, k, v)
        db.session.commit()

app.register_blueprint(scrapebp)

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
