from flask import Flask, render_template, request, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Blueprint
from datetime import datetime
from typing import TYPE_CHECKING

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clubs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# add to support pycharm completion
if TYPE_CHECKING:
    from dataclasses import dataclass as dataclass_sql
else:

    def dataclass_sql(cls):
        return cls


# Settings for migrations
migrate = Migrate(app, db)


@dataclass_sql
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.String(100), db.ForeignKey("club.id"))
    overall_rating = db.Column(db.Float, nullable=False)
    meeting_frequency = db.Column(db.Float, nullable=False)
    club_value = db.Column(db.Float, nullable=False, default=0.0)
    member_count = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200), nullable=True)

    club = db.relationship("Club", backref=db.backref("ratings", lazy=True))


@dataclass_sql
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)

    # Define a relationship to the Club model
    # club = db.relationship('Club', backref=db.backref('events', lazy=True))


@dataclass_sql
class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)

    # Define a relationship to the Club model
    # club = db.relationship('Club', backref=db.backref('officers', lazy=True))


# Now define the Club model after Event and Officer
@dataclass_sql
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
    email = db.Column(db.String(300), nullable=True)
    phonenumber = db.Column(db.String(300), nullable=True)
    categorynames = db.Column(db.String(300), nullable=True)
    pictureblob = db.Column(db.LargeBinary, nullable=True)


@dataclass_sql
class Events(db.Model):
    id = db.Column(db.String(100), nullable=False, primary_key=True)
    clubid = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.Text, nullable=True)
    startsOn = db.Column(db.DateTime, nullable=True)
    endsOn = db.Column(db.DateTime, nullable=True)
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


def load_organization_data(web_key):
    start_marker = "window.initialAppState = "
    end_marker = "</script>"

    club_url = f"https://westernu.campuslabs.ca/engage/organization/{web_key}"
    response = requests.get(club_url)
    if response.status_code == 200:
        start_index = response.text.find(start_marker)
        if start_index < 0:
            return None
        snipped_resp = response.text[start_index + len(start_marker) :]
        snipped_resp = snipped_resp[: snipped_resp.find(end_marker) - 1]
        return json.loads(snipped_resp)["preFetchedData"]["organization"]
    else:
        return None


def scrapepicture(pictureid):
    picture_url = (
        f"https://se-images.campuslabs.ca/clink/images/{pictureid}?preset=med-sq"
    )
    response = requests.get(picture_url)
    if response.status_code == 200:
        return response.content
    else:
        return None


scrapebp = Blueprint("scrape", __name__)


@scrapebp.cli.command("clubs")
def scrape():
    clubs_url = "https://westernu.campuslabs.ca/engage/api/discovery/search/organizations?top=400"
    resp_json = requests.get(clubs_url).json()

    clublist = resp_json["value"]

    for clubResponse in clublist:
        print(clubResponse["Id"])
        cur_club = Club(
            **{
                k.lower(): v
                for k, v in clubResponse.items()
                if k
                in {
                    "Id",
                    "Name",
                    "ProfilePicture",
                    "Summary",
                    "WebsiteKey",
                    "ShortName",
                    "Description",
                    "CategoryNames",
                }
            }
        )
        delimitedCategories = ""
        for category in clubResponse["CategoryNames"]:
            delimitedCategories += category + ";"
        cur_club.categorynames = delimitedCategories
        q_result = db.session.query(Club).where(Club.id == cur_club.id)
        target_row = q_result.first()

        org_data = load_organization_data(cur_club.websitekey)
        if org_data is not None:
            cur_club.youtube = org_data["socialMedia"]["youtubeUrl"]
            cur_club.facebook = org_data["socialMedia"]["facebookUrl"]
            cur_club.linkedin = org_data["socialMedia"]["linkedInUrl"]
            cur_club.twitter = org_data["socialMedia"]["twitterUrl"]
            cur_club.instagram = org_data["socialMedia"]["instagramUrl"]
            cur_club.website = org_data["socialMedia"]["externalWebsite"]
            cur_club.email = org_data["email"]
            if len(org_data["contactInfo"]) >= 1:
                cur_club.phonenumber = org_data["contactInfo"][0]["phoneNumber"]

        if target_row is None:
            cur_club.pictureblob = scrapepicture(cur_club.profilepicture)
            db.session.add(cur_club)
        else:
            if (
                target_row.profilepicture != cur_club.profilepicture
                or target_row.pictureblob is None
            ):
                target_row.pictureblob = scrapepicture(cur_club.profilepicture)
            target_row.name = cur_club.name
            target_row.id = cur_club.id
            target_row.name = cur_club.name
            target_row.profilepicture = cur_club.profilepicture
            target_row.summary = cur_club.summary
            target_row.youtube = cur_club.youtube
            target_row.facebook = cur_club.facebook
            target_row.linkedin = cur_club.linkedin
            target_row.twitter = cur_club.twitter
            target_row.instagram = cur_club.instagram
            target_row.website = cur_club.website
            target_row.email = cur_club.email
            target_row.phonenumber = cur_club.phonenumber
            target_row.websitekey = cur_club.websitekey
            target_row.shortname = cur_club.shortname
            target_row.description = cur_club.description
            target_row.categorynames = cur_club.categorynames
        db.session.commit()


@app.route("/club/<string:club_name>/rate", methods=["POST"])
def rate_club(club_name):
    club = Club.query.filter_by(name=club_name).first()
    if not club:
        abort(404)

    overall_rating_value = request.form.get("overall_rating")
    meeting_frequency_value = request.form.get("meeting_frequency")
    club_value_value = request.form.get("club_value")
    member_count_value = request.form.get("member_count")
    comment_value = request.form.get("comment")

    if (
        not overall_rating_value
        or not meeting_frequency_value
        or not club_value_value
        or not member_count_value
        or not comment_value
    ):
        abort(400)

    try:
        overall_rating_value = float(overall_rating_value)
        meeting_frequency_value = float(meeting_frequency_value)
        club_value_value = float(club_value_value)
        member_count_value = int(member_count_value)
    except ValueError:
        abort(400)

    new_rating = Rating(
        club_id=club.id,
        overall_rating=overall_rating_value,
        meeting_frequency=meeting_frequency_value,
        club_value=club_value_value,
        member_count=member_count_value,
        comment=comment_value,
    )
    db.session.add(new_rating)
    db.session.commit()

    return redirect(url_for("one_club", club_name=club_name))


@app.route("/club/<string:club_name>/ratings")
def get_club_ratings(club_name):
    club = Club.query.filter_by(name=club_name).first()
    if not club:
        abort(404)

    ratings = club.ratings
    average_overall_rating = (
        sum(rating.overall_rating for rating in ratings) / len(ratings)
        if ratings
        else 0
    )
    average_meeting_frequency = (
        sum(rating.meeting_frequency for rating in ratings) / len(ratings)
        if ratings
        else 0
    )
    average_club_value = (
        sum(rating.club_value for rating in ratings) / len(ratings) if ratings else 0
    )
    average_member_count = (
        sum(rating.member_count for rating in ratings) / len(ratings) if ratings else 0
    )
    ratings_with_comments = [
        {
            "rating": rating,
            "comment": rating.comment if rating.comment else "No comment",
        }
        for rating in ratings
    ]

    return render_template(
        "club_ratings.html",
        club=club,
        ratings=ratings_with_comments,
        average_overall_rating=average_overall_rating,
        average_meeting_frequency=average_meeting_frequency,
        average_club_value=average_club_value,
        average_member_count=average_member_count,
    )


@app.route("/club/<club_name>/rating/<rating_id>/edit", methods=["GET", "POST"])
def edit_rating(club_name, rating_id):
    club = Club.query.filter_by(name=club_name).first()
    rating = Rating.query.filter_by(id=rating_id).first()

    if request.method == "POST":
        rating.overall_rating = request.form["overall_rating"]
        rating.meeting_frequency = request.form["meeting_frequency"]
        rating.club_value = request.form["club_value"]
        rating.member_count = request.form["member_count"]
        rating.comment = request.form["comment"]
        db.session.commit()
        return redirect(url_for("one_club", club_name=club_name))

    return render_template("edit_rating.html", club=club, rating=rating)


@app.route("/club/<club_name>/rating/<rating_id>/delete", methods=["POST"])
def delete_rating(club_name, rating_id):
    club = Club.query.filter_by(name=club_name).first()
    rating = Rating.query.filter_by(id=rating_id).first()

    if not club or not rating:
        abort(404)

    db.session.delete(rating)
    db.session.commit()
    return redirect(url_for("one_club", club_name=club_name))


@scrapebp.cli.command("events")
def scrape_events():
    clubs_url = "https://westernu.campuslabs.ca/engage/api/discovery/event/search?endsBefore=2028-07-21T20%3A00%3A57-04%3A00&orderByField=endsOn&orderByDirection=descending&status=Approved&take=100&query=&skip=0&organizationIds%5B0%5D="

    ci = 0
    clubs = Club.query.all()

    for c in clubs:
        if ci > 3:
            break
        ci += 1
        resp_json = requests.get(clubs_url + c.id).json()

        eventlist = resp_json["value"]  # Access events directly from the 'value' key

        for ev in eventlist:
            print(ev["id"])
            cur_ev = Events(
                **{
                    k: v
                    for k, v in ev.items()
                    if k
                    in {
                        "id",
                        "name",
                        "description",
                        "location",
                        "startsOn",
                        "endsOn",
                        "imagePath",
                        "pictureblob",
                        "theme",
                        "categorynames",
                        "latitude",
                        "longitude",
                    }
                }
            )
            cur_ev.clubid = c.id
            cur_ev.startsOn = datetime.strptime(
                ev["startsOn"], "%Y-%m-%dT%H:%M:%S+00:00"
            )
            cur_ev.endsOn = datetime.strptime(ev["endsOn"], "%Y-%m-%dT%H:%M:%S+00:00")
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
                if (
                    target_row.imagePath != cur_ev.imagePath
                    or target_row.pictureblob is None
                ):
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


app.register_blueprint(scrapebp)


@app.route("/")
def index():
    search_query = request.args.get("search")

    clubs = Club.query

    if search_query:
        clubs = clubs.filter(
            (Club.name.contains(search_query))
            | (Club.websitekey.contains(search_query))
            | (Club.shortname.contains(search_query))
            | (Club.categorynames.contains(search_query))
        )

    clubs = clubs.all()
    return render_template("index.html", clubs=clubs)


@app.route("/club/<string:club_name>")
def one_club(club_name):
    club = Club.query.filter_by(name=club_name).first()
    if not club:
        abort(404)

    ratings = club.ratings
    average_overall_rating = round(
        sum(rating.overall_rating for rating in ratings) / len(ratings)
        if ratings
        else 0,
        1,
    )
    average_meeting_frequency = round(
        sum(rating.meeting_frequency for rating in ratings) / len(ratings)
        if ratings
        else 0,
        1,
    )
    average_club_value = round(
        sum(rating.club_value for rating in ratings) / len(ratings) if ratings else 0, 1
    )
    average_member_count = (
        sum(rating.member_count for rating in ratings) / len(ratings) if ratings else 0
    )

    return render_template(
        "club_page.html",
        club=club,
        average_overall_rating=average_overall_rating,
        average_meeting_frequency=average_meeting_frequency,
        average_club_value=average_club_value,
        average_member_count=average_member_count,
    )


@app.route("/clubprofilepic/<string:club_name>")
def fetchprofilepic(club_name):
    club = Club.query.filter_by(name=club_name).first()
    if not club:
        abort(404)
    return club.pictureblob, 200, {"Content-Type": "image/png"}


if __name__ == "__main__":
    app.run(debug=True)
