import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

from sqlalchemy.sql import func

app = Flask(__name__)

static_studs = [
    {
        "id": 1,
        "name": "Club A",
        "shortbio": "Short description of Club A.",
        "bio": "Long description of Club A. This can include information about the club's history, goals, activities, etc.",
        "contact": "cluba@gmail.com",
        "events": [
            {
                "date": "2024-07-10",
                "title": "Club A Meeting"
            },
            {
                "date": "2024-07-15",
                "title": "Club A Event"
            }
        ],
        "officers": [
            {
                "name": "John Doe",
                "position": "President"
            },
            {
                "name": "Jane Smith",
                "position": "Vice President"
            }
        ]
    },
    {
        "id": 2,
        "name": "Club B",
        "shortbio": "Short description of Club B.",
        "bio": "Long description of Club B.",
        "contact": "clubb@gmail.com",
        "events": [],
        "officers": []
    }
    # Add more clubs as needed
]

@app.route('/')
def index():
    return render_template('index.html', clubs = static_studs)

@app.route('/club/<int:club_id>')
def one_club(club_id):
    the_club = next((item for item in static_studs if item["id"] == club_id), None)
    return render_template('club_page.html', club = the_club)




