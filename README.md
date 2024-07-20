# Rate My Clubs

## Overview

**Rate My Clubs** is a web application designed for students at Western University of Ontario to rate and review various student clubs and organizations. The concept is similar to "Rate My Professors" but tailored for student clubs, providing a platform where students can share their experiences and insights about the clubs they are involved in.

## Purpose

The primary goal of this project is to create a centralized platform where students can:
- Discover and learn about different clubs and organizations at Western University.
- Rate clubs based on various criteria such as value, member engagement, and activities.
- Leave comments and feedback about their experiences with the clubs.
- View ratings and feedback from other students.

## Features

1. **Web Scraper and Database Integration**:
   - Utilizing the API provided by Western University's official club list, this application scrapes and imports the necessary data into a structured database. 
   - The information collected includes club names, officers, descriptions, and contact details.
   - The scraper runs periodically to check for updates on the official website and automatically updates the database to reflect any changes.

2. **User Interface**:
   - A user-friendly web interface built with Flask, allowing users to browse through the clubs.
   - Each club has a dedicated page displaying detailed information and user-generated ratings and comments.
   - Clubs are displayed in an easily navigable format, with clickable cards leading to more detailed pages.

3. **Rating and Commenting System**:
   - Users can rate clubs on various criteria.
   - Users can leave comments sharing their personal experiences and feedback.

## Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (using SQLAlchemy for ORM)
- **Web Scraping**: Requests and JSON for API interaction
- **Frontend**: HTML, CSS

## Future Enhancements
- **Clean up Respository**: Yes the repo is super cluttered right now, will clean it up as I go and learn!!
- **Advanced Filtering and Search**: Implementing advanced filtering and search functionalities to help users find clubs that match their interests.
- **Enhanced Rating System**: Adding more detailed rating categories and aggregate scores.
- **User Authentication**: Enabling user registration and login to personalize the experience and manage contributions.
- **Remove Clubs From Database if Not in Official Website**: Detect if a website has been deleted from the official western website and update the database accordingly.


## View Database Contents

```bash
cd instance
sqlite3 clubs.db
.mode column
.headers on
select name,shortname, websitekey from club;
```
## Migrations to Update Tables

```bash
flask db migrate -m "DATABASE COMMENT HERE"
flask db upgrade
```
