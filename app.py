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
    shortname = db.Column(db.String(100), nullable=True)
    summary = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    contact = db.Column(db.String(100), nullable=True)
    instagram = db.Column(db.String(100), nullable=True)
    youtube = db.Column(db.String(100), nullable=True)
    linkedin = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    facebook = db.Column(db.String(100), nullable=True)
    twitter = db.Column(db.String(100), nullable=True)
    categorynames = db.Column(db.String(300), nullable=True)
    pictureblob = db.Column(db.LargeBinary, nullable=True)
    
class Events(db.Model):
    id = db.Column(db.String(100), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.Text, nullable=True)
    startsOn = db.Column(db.DateTime, nullable = True)
    endsOn = db.Column(db.DateTime, nullable = True)
    imagePath = db.Column(db.String(100), nullable=True)
    pictureblob = db.Column(db.LargeBinary, nullable=True)
    theme = db.Column(db.Text, nullable=True)
    categorynames = db.Column(db.String(300), nullable=True)
    latitude = db.Column(db.Text, nullable=True)
    longitude = db.Column(db.Text, nullable=True)


import json
import requests

# Roster
# https://westernu.campuslabs.ca/engage/organization/%7B%7BWebsiteKey%7D%7D/roster
# window.initialAppState = {
# ...
# };

# Event RSS feed
# https://westernu.campuslabs.ca/engage/organization/associationofroleplayers/events.rss

# Past events
# https://westernu.campuslabs.ca/engage/api/discovery/event/search
# endsBefore=2024-07-21T20%3A00%3A57-04%3A00
# &orderByField=endsOn
# &orderByDirection=descending
# &status=Approved
# &take=15
# &query=
# &skip=0
# &organizationIds%5B0%5D=1746

# https://westernu.campuslabs.ca/engage/api/discovery/event/search
# endsAfter=2024-07-21T20%3A06%3A57-04%3A00
# &orderByField=endsOn
# &orderByDirection=ascending
# &status=Approved
# &take=15
# &query=
# &skip=0
# &organizationIds%5B0%5D=1746

def scrapepicture(pictureid):
        picture_url = f"https://se-images.campuslabs.ca/clink/images/{pictureid}?preset=med-sq"
        response = requests.get(picture_url)
        if response.status_code == 200:
            return response.content
        else:
            return None

scrapebp = Blueprint('scrape', __name__)

@scrapebp.cli.command('clubs')
def scrape():
    clubs_url = "https://westernu.campuslabs.ca/engage/api/discovery/search/organizations?top=400"
    resp_json = requests.get(clubs_url).json()

    clublist = resp_json["value"]

    for clubResponse in clublist:
        print(clubResponse["Id"])
        cur_club = Club(**{k.lower():v for k, v in clubResponse.items() if k in {'Id', 'Name', 'ProfilePicture', 'Summary', 'WebsiteKey', 'ShortName', 'Description', 'CategoryNames'}})
        delimitedCategories = ""
        for category in clubResponse["CategoryNames"]:
            delimitedCategories += category + ";"
        cur_club.categorynames = delimitedCategories
        q_result = db.session.query(Club).where(Club.id == cur_club.id)
        target_row = q_result.first()
        if target_row is None:
            cur_club.pictureblob = scrapepicture(cur_club.profilepicture)
            db.session.add(cur_club)
        else:
            if target_row.profilepicture != cur_club.profilepicture or target_row.pictureblob is None:
                target_row.pictureblob = scrapepicture(cur_club.profilepicture)
            target_row.name = cur_club.name
            target_row.id = cur_club.id
            target_row.name = cur_club.name
            target_row.profilepicture = cur_club.profilepicture
            target_row.summary = cur_club.summary
            target_row.websitekey = cur_club.websitekey
            target_row.shortname = cur_club.shortname
            target_row.description = cur_club.description
            target_row.categorynames = cur_club.categorynames
        db.session.commit()
        
app.register_blueprint(scrapebp)

@scrapebp.cli.command('events')
def scrape_events():
    clubs_url = "https://westernu.campuslabs.ca/engage/api/discovery/event/search?endsBefore=2028-07-21T20%3A00%3A57-04%3A00&orderByField=endsOn&orderByDirection=descending&status=Approved&take=100&query=&skip=0&organizationIds%5B0%5D="

    ci = 0
    clubs = Club.query.all()

    for c in clubs:
        if ci > 10:
            break
        ci += 1
        resp_json = requests.get(clubs_url + c.id).json()

        eventlist = resp_json["value"]

        for ev in eventlist:
            print(ev["id"])
            cur_ev = Events(**{k.lower():v for k, v in eventlist.items() if k in { 'id',  'name',  'description',  'location',  'startsOn', 'endsOn', 'imagePath', 'pictureblob', 'theme', 'categorynames', 'latitude', 'longitude' }})
            delimitedCategories = ""
            for category in ev["categoryNames"]:
                delimitedCategories += category + ";"
            cur_ev.categorynames = delimitedCategories
            q_result = db.session.query(Events).where(Events.id == cur_ev.id)
            target_row = q_result.first()
            if target_row is None:
                cur_ev.pictureblob = scrapepicture(cur_ev.imagePath)
                db.session.add(cur_ev)
            else:
                if target_row.imagePath != cur_ev.i or target_row.pictureblob is None:
                    target_row.pictureblob = scrapepicture(cur_ev.imagePath)
                target_row.name = cur_ev.name
                target_row.id = cur_ev.id
                target_row.name = cur_ev.name
                target_row.description = cur_ev.description
                target_row.location = cur_ev.location
                target_row.startsOn = cur_ev.startsOn 
                target_row.endsOn = cur_ev.endsOn 
                target_row.imagePath = cur_ev.imagePath 
                target_row.theme = cur_ev.theme 
                target_row.categorynames = cur_ev.categorynames 
                target_row.latitude = cur_ev.latitude 
                target_row.longitude = cur_ev.longitude 

            db.session.commit()

@app.route('/')
def index():
    search_query = request.args.get('search')
    
    clubs = Club.query

    if search_query:
        clubs = clubs.filter(
            (Club.name.contains(search_query)) |
            (Club.websitekey.contains(search_query)) |
            (Club.shortname.contains(search_query)) |
            (Club.categorynames.contains(search_query))
        )

    clubs = clubs.all()
    return render_template('index.html', clubs=clubs)


@app.route('/club/<string:club_name>')
def one_club(club_name):
    club = Club.query.filter_by(name=club_name).first()
    if not club:
        abort(404)
    return render_template('club_page.html', club=club)

@app.route('/clubprofilepic/<string:club_name>')
def fetchprofilepic(club_name):
    club = Club.query.filter_by(name=club_name).first()
    if not club:
        abort(404)
    return club.pictureblob, 200, {'Content-Type': 'image/png'}
    
if __name__ == "__main__":
    app.run(debug=True)
