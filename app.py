from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
import database
import os
import secrets
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DEFAULT_IMAGE'] = 'static/img/default.jpg'  # Path to your default image
app.config['SECRET_KEY'] = secrets.token_hex(16) 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# --- Helper Functions ---

def get_current_user():
    player_id = session.get("player_id")
    if player_id:
        return database.get_player(player_id)
    return None

# --- User Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_number = request.form.get('player_number')
        if not player_number:
            flash('Player number is required', 'error')
            return redirect(url_for('index'))

        player = database.get_player_by_number(player_number)

        if player:
            # Player exists
            session["player_id"] = player["id"]
            if not player['photo'] or player['photo'] == app.config['DEFAULT_IMAGE']:
                # Redirect to photo upload if no photo or default photo
                return redirect(url_for('upload_photo'))
            else:
                return redirect(url_for('leaderboard'))
        else:
            # Player does not exist
            flash('Invalid player number. Please register.', 'error')
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    player = get_current_user()
    if not player:
        return redirect(url_for("index"))

    if request.method == 'POST':
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                filename = str(player['player_number']) + "_" + photo.filename
                # Use os.path.join for proper path construction
                full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\", "/")
                photo.save(full_path)
                photo_path = full_path.replace("\\", "/")
                database.update_player_photo(player['id'], photo_path)
                flash('Photo uploaded successfully!', 'success')
                return redirect(url_for('leaderboard'))
            else:
                flash('No photo selected.', 'error')
        else:
            flash('No photo selected.', 'error')

    return render_template('upload_photo.html')

@app.route('/leaderboard')
def leaderboard():
    player = get_current_user()
    if not player:
        return redirect(url_for("index"))
    players = database.get_all_players()
    games = database.get_all_games()  # Get the list of games
    game_results = database.get_all_game_results()  # Get game results
    return render_template('leaderboard.html', players=players, current_player=player, games=games, game_results=game_results, is_player_eliminated=database.is_player_eliminated)

@app.route('/games')
def game_timeline():
    player = get_current_user()
    if not player:
        return redirect(url_for("index"))
    games = database.get_all_games()
    player_teams = database.get_player_teams(player['id'])
    players = database.get_all_players()
    game_results = database.get_all_game_results()
    return render_template('game_timeline.html', games=games, player_teams=player_teams, current_player=player, players=players, game_results=game_results)

@app.route('/register_team', methods=['POST'])
def register_team():
    player = get_current_user()
    if not player:
        return redirect(url_for("index"))

    game_name = request.form.get('game_name')
    team_name = request.form.get('team_name')
    
    # Validate team size based on game
    if game_name == '1-2-1-2':
        # Check if the player is already in a team for this game
        existing_team = database.get_player_team_for_game(player['id'], game_name)
        if existing_team:
            return "You are already registered in a team for this game.", 400

        team_members = request.form.getlist('team_members[]')
        if len(team_members) != 4:  # 4 members + the creator
            return "Team must have exactly 5 members for 1-2-1-2.", 400
        # Check if any selected member is already in another team for the same game
        for member_id in team_members:
            if database.get_player_team_for_game(member_id, game_name):
                return "One or more selected members are already in a team for this game.", 400

        team_id = database.create_team(game_name, team_name)
        database.add_team_member(team_id, player['id'])
        for member_id in team_members:
            database.add_team_member(team_id, int(member_id))

    elif game_name == 'Mocador':
        existing_team = database.get_player_team_for_game(player['id'], game_name)
        if existing_team:
            return "You are already registered in a team for this game.", 400
        team_id = database.create_team(game_name, team_name)
        database.add_team_member(team_id, player['id'])

    return redirect(url_for('game_timeline'))


@app.route('/vote/<int:player_id>', methods=['POST'])
def vote_final(player_id):
    player = get_current_user()
    if not player:
        return redirect(url_for("index"))
    final_game = database.get_game_by_name("Final: Preguntes")
    if final_game and final_game['status'] == 'ongoing':
      database.add_vote_to_player(player_id)
      flash('Vote submitted successfully!', 'success')
      return redirect(url_for('game_timeline'))
    else:
      return "Voting is not available at the moment", 400


@app.route('/profile/<int:player_id>')
def player_profile(player_id):
    player = get_current_user()
    if not player:
        return redirect(url_for("index"))
    profile_player = database.get_player(player_id)
    if not profile_player:
        # Handle case where player doesn't exist
        return "Player not found", 404
    game_results = database.get_player_game_results(player_id)
    player_teams = database.get_player_teams(player_id)

    return render_template('player_profile.html', profile_player=profile_player, game_results=game_results, player_teams=player_teams, current_player=player)
  


@app.route('/join_team/<int:team_id>', methods=['POST'])
def join_team(team_id):
    player = get_current_user()
    if not player:
        return redirect(url_for("index"))
    team = database.get_team(team_id)
    
    # Prevent joining a team of a different game

    print(team_id)
    if team['game_name'] != 'Mocador':
        return "You can only join Mocador teams.", 400
    
    # Check if player is already in a team for this game
    if any(t['game_name'] == 'Mocador' for t in database.get_player_teams(player['id'])):
        return "You are already in a Mocador team.", 400
    
    database.add_team_member(team_id, player['id'])
    return redirect(url_for('game_timeline'))

# --- Admin Routes ---
@app.context_processor
def inject_mocador_teams():
    def get_mocador_teams():
        return database.get_all_teams_by_game_name('Mocador')
    return dict(get_mocador_teams=get_mocador_teams)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if database.check_admin_credentials(username, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
            # Redirect to admin login on failed login attempt
            return redirect(url_for('admin_login'))

    return render_template('admin/login.html')
@app.route('/admin/logout')
def admin_logout():
  session.pop('admin_logged_in', None)
  return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    players = database.get_all_players()
    games = database.get_all_games()
    return render_template('admin/index.html', players=players, games=games)

@app.route('/search_players')
def search_players():
    query = request.args.get('q')
    if query:
        # Search for players by number (or name if you have it)
        # Exclude players who are already in a 1-2-1-2 team
        players = database.search_players_by_number(query)  # You'll need to implement this function in database.py
        # Filter out players already in a 1-2-1-2 team
        available_players = [
            p for p in players if not database.get_player_team_for_game(p['id'], '1-2-1-2')
        ]
        return jsonify(available_players)
    return jsonify([])

@app.route('/admin/players')
def manage_players():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    players = database.get_all_players()
    teams = database.get_all_teams()
    games = database.get_all_games()  # Fetch the games
    return render_template('admin/manage_players.html', players=players, teams=teams, games=games, is_player_eliminated=database.is_player_eliminated)

@app.route('/admin/games')
def manage_games():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    games = database.get_all_games()
    return render_template('admin/manage_games.html', games=games)

@app.route('/admin/update_score', methods=['POST'])
def update_score():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    player_id = request.form.get('player_id')
    points = int(request.form.get('points'))
    database.update_player_score(player_id, points)
    return redirect(url_for('manage_players'))

@app.route('/admin/update_team_score', methods=['POST'])
def update_team_score():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    team_id = request.form.get('team_id')
    points = int(request.form.get('points'))
    database.update_team_score(team_id, points)
    return redirect(url_for('manage_players'))

@app.route('/admin/eliminate_player', methods=['POST'])
def eliminate_player():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    player_id = request.form.get('player_id')
    game_id = request.form.get('game_id')
    action = request.form.get('action')  # Get the action (either 'eliminate' or 'uneliminate')

    if action == 'eliminate':
        if database.eliminate_player(player_id, game_id):
            flash('Player eliminated successfully.', 'success')
        else:
            flash('Error eliminating player.', 'error')
    elif action == 'uneliminate':
        if database.uneliminate_player(player_id, game_id):
            flash('Player uneliminated successfully.', 'success')
        else:
            flash('Error uneliminating player.', 'error')
    else:
        flash('Invalid action specified.', 'error')

    return redirect(url_for('manage_players'))

@app.route('/admin/game/<int:game_id>/reveal', methods=['POST'])
def reveal_game(game_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    database.update_game_status(game_id, 'revealed')
    return redirect(url_for('manage_games'))

@app.route('/admin/game/<int:game_id>/complete', methods=['POST'])
def complete_game(game_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    database.update_game_status(game_id, 'completed')
    return redirect(url_for('manage_games'))

@app.route('/admin/game/<int:game_id>/start_voting', methods=['POST'])
def start_voting(game_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    database.update_game_status(game_id, 'ongoing')
    return redirect(url_for('manage_games'))

@app.route('/admin/create_game', methods=['POST'])
def create_game():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    name = request.form.get('name')
    type = request.form.get('type')
    max_players = request.form.get('max_players')
    if database.create_game(name, type, max_players):
        flash('Game created successfully!', 'success')
    else:
        flash('Error creating game. A game with that name might already exist.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/game/<int:game_id>/start', methods=['POST'])
def start_game(game_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    database.update_game_status(game_id, 'revealed')
    flash('Game started!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/create_team', methods=['POST'])
def admin_create_team():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    game_name = request.form.get('game_name')
    team_name = request.form.get('team_name')
    team_id = database.create_team(game_name, team_name)
    if team_id:
        flash(f'Team "{team_name}" created successfully for game "{game_name}".', 'success')
    else:
        flash(f'Error creating team. Ensure the game name is correct and the team name is unique for that game.', 'error')
    return redirect(url_for('manage_players'))

@app.route('/admin/add_team_member', methods=['POST'])
def admin_add_team_member():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    team_id = request.form.get('team_id')
    player_id = request.form.get('player_id')
    if database.add_team_member(team_id, player_id):
        flash('Player added to team successfully.', 'success')
    else:
        flash('Error adding player to team. Ensure the player is not already in a team for this game.', 'error')
    return redirect(url_for('manage_players'))

@app.route('/admin/remove_team_member', methods=['POST'])
def admin_remove_team_member():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    team_id = request.form.get('team_id')
    player_id = request.form.get('player_id')
    if database.remove_team_member(team_id, player_id):
        flash('Player removed from team successfully.', 'success')
    else:
        flash('Error removing player from team.', 'error')
    return redirect(url_for('manage_players'))

@app.route('/admin/delete_team/<int:team_id>', methods=['POST'])
def admin_delete_team(team_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    if database.delete_team(team_id):
        flash('Team deleted successfully.', 'success')
    else:
        flash('Error deleting team.', 'error')
    return redirect(url_for('manage_players'))

@app.route('/admin/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    try:
        database.delete_player(player_id)
        flash('Player deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting player: {e}', 'error')

    return redirect(url_for('manage_players'))

@app.route('/admin/delete_game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    if database.delete_game(game_id):
        flash('Game deleted successfully.', 'success')
    else:
        flash('Error deleting game.', 'error')
    return redirect(url_for('manage_games'))

@app.route('/admin/game/<int:game_id>/restart', methods=['POST'])
def restart_game(game_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    if database.update_game_status(game_id, 'hidden'):
        flash('Game restarted successfully.', 'success')
    else:
        flash('Error restarting game.', 'error')
    return redirect(url_for('manage_games'))

# --- Initialize the Database ---
with app.app_context():
    database.init_db()
    database.add_admin('admin1', 'caigei29')
    database.create_game('Pica Paret', 'Classifying', 80)
    database.create_game('1-2-1-2', 'Classifying', 80)
    database.create_game('Mocador', 'Classifying', 80)
    database.create_game('Fet i amagar', 'Eliminatory', 60)
    database.create_game('Fer grups', 'Eliminatory', 60)
    database.create_game('Cadires', 'Eliminatory', 60)
    database.create_game('Beerpong', 'Eliminatory', 60)
    database.create_game('Final: Preguntes', 'Eliminatory', 60)
    database.prepopulate_players(database.player_names)

    

if __name__ == '__main__':
    app.run(debug=True)
