# ⭐ Rate My Clubs 

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

4. **Microsoft University Email Single Sign On**:
   - Instead of requiring account creation, students can simply sign on to Rate My Clubs using their university email address.
   - Accounts will be tied to the university email address

## Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (using SQLAlchemy for ORM)
- **Web Scraping**: Requests and JSON for API interaction
- **Frontend**: HTML, CSS

## Roadmap:

- ✅ **Set up scraping engine**: Create a scraper that reads the website's HTML and essentially copies the club information over onto this website. 
- ✅ **CRUD rating system**: Rating system that allows users to create, edit, and delete personalized ratings with multiple criteria. 
- **Implement Tailwind Framework**: Cleanup the current CSS and use Tailwind or some sort of framework.
- **Clean up repository**: Don't worry I'll make sure this mess gets organized soon
- **Average rating display**: Display the average rating of clubs on individual club cards when scrolling through the club finder list.
- **Improved filtering and searching**: Implementing advanced filtering and search functionalities to help users find clubs that match their interests.
- **Microsoft WesternIdentity SSO**: Allow students to easily login to the platform with their UWO email address.

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
