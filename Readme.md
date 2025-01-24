
# Squid Games Web Application
> Inspired by the Netflix series *The Squid Games* we created the *Jocs de l'oreneta*, which consisted in different games in which players participated, which ended up with a winner. This website allowed us to control them.

## Overview
This project is a Flask-based web application inspired by the Squid Games concept, to control the *Jocs de l'oreneta*. The application allows users to view timelines, player profiles, leaderboards, and manage content through an admin interface. It also provides functionality for uploading photos and managing game data.

## Project Structure

```
flask_session/           # Flask session-related files (e.g., session data)

static/                  # Static files for the web application
  css/                   # CSS files for styling
    style.css            # Main stylesheet
  fonts/                 # Fonts used in the application
  img/                   # Images used in the application
  js/                    # JavaScript files
    admin.js             # Admin-specific JavaScript functionality
    scripts.js           # General JavaScript functionality
  uploads/               # Directory for uploaded files

templates/               # HTML templates for rendering pages
  admin/                 # Templates for admin pages
  admin.html             # Admin dashboard template
  game_timeline.html     # Template for displaying the game timeline
  index.html             # Homepage template
  leaderboard.html       # Template for displaying the leaderboard
  player_profile.html    # Template for player profiles
  upload_photo.html      # Template for uploading photos

venv/                    # Virtual environment for managing dependencies

.gitignore               # Git ignore file
app.py                   # Main Flask application entry point
database.py              # Database interaction logic
Procfile                 # Configuration for deploying to Heroku or similar platforms
Readme.md                # Documentation file (this file)
requirements.txt         # Python dependencies
schema.sql               # SQL schema for setting up the database
squid_games.db           # SQLite database file
```

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application in your browser at `http://127.0.0.1:5000/`, or admin at `http://127.0.0.1:5000/admin`

## Key Features

- **Game Timeline**: Displays the sequence activities in the game.
- **Player Profiles**: View details about individual players.
- **Leaderboard**: Ranks players based on their performance.
- **Eliminatory Leaderboard**: Shows players who have been eliminated.
- **Admin Dashboard**: Manage the game, players, and content.
- **Photo Uploads**: Upload images for player profiles or other purposes.

## Deployment

The application was deployed to [Heroku](https://www.heroku.com/). Use the `Procfile` for deployment configuration (it is pretty straightforward).

To deploy with Heroku, install the Heroku CLI, initialize a git repository, set up the app and push the contents of the directory.

## Images
![alt text](</images/WhatsApp Image 2025-01-21 at 04.24.37.jpeg>)
![alt text](</images/WhatsApp Image 2025-01-21 at 04.24.37 (1).jpeg>)
![alt text](</images/WhatsApp Image 2025-01-21 at 04.24.37 (2).jpeg>)
![alt text](/images/IMG_20250124_192256.jpg)

## License

This project is licensed under the MIT License. Feel free to use it in any way you want.

