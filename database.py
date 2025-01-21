import sqlite3

DB_NAME = 'squid_games.db'

def prepopulate_players(player_names):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    for i, name in enumerate(player_names):
        player_number = i + 1
        try:
            cursor.execute("INSERT INTO players (player_number, name, photo, score) VALUES (?, ?, ?, ?)",
                           (player_number, name, 'static/img/default.jpg', 0))
            print(f"Added player: {name} with number {player_number}")
        except sqlite3.IntegrityError:
            print(f"Player with number {player_number} already exists. Skipping.")

    db.commit()
    db.close()

player_names = [
    "Abril Risso Matas",
    "Adrià Flores",
    "Alba Figueras Fernández",
    "Aleix Ibars",
    "Alex Navarro Navarro",
    "Alex Latorre",
    "Andres Gonzalez V",
    "Andreu Lopez Perez",
    "Anna Casanovas Poirier",
    "Anna Galstyan Galoyan",
    "Berta Aulet",
    "Berta Vidal Gómez",
    "Cai Selvas Sala",
    "Carla Atienza",
    "Carlos Nieves Montes",
    "Carlos Palazón Domingo",
    "Cesar Elias Mejia Rota",
    "Claudia Gallego Torralbo",
    "Daniel López García",
    "Daniel Pastor Miguel",
    "Elies Aragonès Larrañaga",
    "Pau Escobar Asensio",
    "Eva Martinez Martinez",
    "Fabián Birch Torrejón",
    "Ferran Òdena Bernadí",
    "Guillem Arnau Vallejos Clavell",
    "Guillem Figueruelo Arias",
    "Hugo Ortí Toledo",
    "Ilyas Ouacham Rhailane",
    "Irene Miralles Ortega",
    "Irene Pumares",
    "Jan Estrada Morant",
    "Javier Aranda Fernández",
    "Jan Bennàssar Martín",
    "Joan Bernaus Casadesús",
    "Joan Riera Tur",
    "Laia Beyloc Guzmán",
    "Lihao Jin Wang",
    "Lluc Furriols Llimargas",
    "Lola Monroy Mir",
    "Lucía Álvarez",
    "Maria Gil Casas",
    "Marie-Anne Boter Plana",
    "Marina Teruel Olmedo",
    "Mariona Casasnovas Simon",
    "Marta Carrión",
    "Marta Juncarol Pi",
    "Marta Nadal Par",
    "Martí Andreu Teixidor",
    "Martí Pujadas Moreno",
    "Mattias Fuguet Yandell",
    "Max Mira García",
    "Máximo Meya Morales",
    "Miquel Rodríguez Sansaloni",
    "Miquel Ropero Serrano",
    "Mireia Brichs Ralló",
    "Nicolás Rosales Gómez",
    "Núria Llopart",
    "Núria López Encinas",
    "Oriol Martí Sanahuja",
    "Oscar Mata Segura",
    "Pablo Aviles Perez",
    "Pablo González Monfort",
    "Pablo Chacón Martín",
    "pau aboal",
    "Pau Prat Moreno",
    "Paula Esteve Sabater",
    "Pengcheng Chen",
    "Pol Margarit Fisas",
    "Pol Pérez Prades",
    "Pol Riera Mcardle",
    "Robert Ennakhli Ostrozhinskiy",
    "Roger Baiges",
    "Rubén Álvarez Aragonés",
    "Sergi Flores Marín",
    "Uriel Gil Palma",
    "Verónica Oñate Villagrasa",
    "Violeta Bonet Vila"
]


def get_db():
    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row  # Access columns by name
    return db

def init_db():
    db = get_db()
    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    cursor = db.cursor()
    mocador_teams = [
        ('Mocador',1),
        ('Mocador', 2),
        ('Mocador', 3),
        ('Mocador', 4)
    ]
    for game_name, team_name in mocador_teams:
        if not get_team_id_by_name(game_name, team_name):
            cursor.execute("INSERT INTO teams (game_name, team_name) VALUES (?, ?)", (game_name, team_name))
    db.commit()
    db.close()
    db.close()

def create_player(player_number, photo_path):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO players (player_number, photo) VALUES (?, ?)", (player_number, photo_path))
    player_id = cursor.lastrowid
    db.commit()
    db.close()
    return player_id

def update_player_photo(player_id, photo_path):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE players SET photo = ? WHERE id = ?", (photo_path, player_id))
    db.commit()
    db.close()

def get_player_by_number(player_number):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM players WHERE player_number = ?", (player_number,))
    player = cursor.fetchone()
    db.close()
    return player

def get_player(player_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
    player = cursor.fetchone()
    db.close()
    return player

def get_all_players():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM players ORDER BY score DESC")
    players = cursor.fetchall()
    db.close()
    return players

def update_player_score(player_id, points):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE players SET score = score + ? WHERE id = ?", (points, player_id))
    db.commit()
    db.close()

def get_all_games():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    db.close()
    return games

def get_game_by_name(game_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM games WHERE name = ?", (game_name,))
    game = cursor.fetchone()
    db.close()
    return game

def delete_game(game_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # First, delete related records in game_results (optional, depending on your requirements)
        cursor.execute("DELETE FROM game_results WHERE game_id = ?", (game_id,))

        print("Deleting game")
        # Then, delete the game
        cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
        db.commit()
        return True
    except Exception as e:
        print(f"Error deleting game: {e}")
        return False
    finally:
        db.close()

def update_game_status(game_id, status):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE games SET status = ? WHERE id = ?", (status, game_id))
        db.commit()
        return True
    except Exception as e:
        print(f"Error updating game status: {e}")
        return False
    finally:
        db.close()


def get_player_game_results(player_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT g.name, gr.result
        FROM game_results gr
        JOIN games g ON gr.game_id = g.id
        WHERE gr.player_id = ?
    """, (player_id,))
    results = cursor.fetchall()
    db.close()
    return results

def create_team(game_name, team_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO teams (game_name, team_name) VALUES (?, ?)", (game_name, team_name))
    team_id = cursor.lastrowid
    db.commit()
    db.close()
    return team_id

def add_team_member(team_id, player_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO team_members (team_id, player_id) VALUES (?, ?)", (team_id, player_id))
    db.commit()
    db.close()

def get_player_team_for_game(player_id, game_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT t.* 
        FROM teams t
        JOIN team_members tm ON t.id = tm.team_id
        WHERE tm.player_id = ? AND t.game_name = ?
    """, (player_id, game_name))
    team = cursor.fetchone()
    db.close()
    return team

def get_team(team_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = cursor.fetchone()
    db.close()
    return team

def get_player_teams(player_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT t.* 
        FROM teams t
        JOIN team_members tm ON t.id = tm.team_id
        WHERE tm.player_id = ?
    """, (player_id,))
    teams = cursor.fetchall()
    db.close()
    return teams

def update_team_score(team_id, points):
    db = get_db()
    cursor = db.cursor()
    # Update the score for all team members
    cursor.execute("""
        UPDATE players
        SET score = score + ?
        WHERE id IN (SELECT player_id FROM team_members WHERE team_id = ?)
    """, (points, team_id))
    db.commit()
    db.close()

def eliminate_player(player_id, game_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO game_results (game_id, player_id, result) VALUES (?, ?, 'eliminated')", (game_id, player_id))
    # Optionally, adjust the player's score or status if needed
    db.commit()
    db.close()

def add_vote_to_player(player_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE players SET score = score + 1 WHERE id = ?", (player_id,))
    db.commit()
    db.close()

#Admin functions

def check_admin_credentials(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
    admin = cursor.fetchone()
    db.close()
    return admin is not None


def get_all_teams_by_game_name(game_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM teams WHERE game_name = ?", (game_name,))
    teams = cursor.fetchall()
    db.close()
    return teams

def add_admin(username, password):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO admins (username, password) VALUES (?,?)", (username, password))
        db.commit()
    except sqlite3.IntegrityError:
        # User already exists, update the password instead
        cursor.execute("UPDATE admins SET password = ? WHERE username = ?", (password, username))
        db.commit()
        print(f"Password for admin '{username}' updated successfully.")
    finally:
        db.close()


def create_game(name, type, max_players):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO games (name, type, max_players) VALUES (?, ?, ?)", (name, type, max_players))
        db.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Error: Game with name '{name}' already exists.")
        return None
    finally:
        db.close()

def create_team(game_name, team_name):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO teams (game_name, team_name) VALUES (?, ?)", (game_name, team_name))
        team_id = cursor.lastrowid
        db.commit()
        return team_id
    except sqlite3.IntegrityError:
        print(f"Error: Team with name '{team_name}' already exists for game '{game_name}'.")
        return None
    finally:
        db.close()

def add_team_member(team_id, player_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # Check if the player is already in a team for the same game
        cursor.execute("SELECT tm.team_id FROM team_members tm JOIN teams t ON tm.team_id = t.id WHERE tm.player_id = ? AND t.game_name = (SELECT game_name FROM teams WHERE id = ?)", (player_id, team_id))
        existing_team = cursor.fetchone()
        if existing_team:
            print(f"Error: Player is already in a team for this game.")
            return False

        cursor.execute("INSERT INTO team_members (team_id, player_id) VALUES (?, ?)", (team_id, player_id))
        db.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error adding player to team: {e}")
        return False
    finally:
        db.close()

def remove_team_member(team_id, player_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM team_members WHERE team_id = ? AND player_id = ?", (team_id, player_id))
        db.commit()
        return True
    except Exception as e:
        print(f"Error removing player from team: {e}")
        return False
    finally:
        db.close()


def uneliminate_player(player_id, game_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM game_results WHERE player_id = ? AND result = 'eliminated'", (player_id,))
        db.commit()
        return True
    except Exception as e:
        print(f"Error uneliminating player: {e}")
        return False
    finally:
        db.close()

def delete_team(team_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # First, remove all members from the team
        cursor.execute("DELETE FROM team_members WHERE team_id = ?", (team_id,))
        # Then, delete the team itself
        cursor.execute("DELETE FROM teams WHERE id = ?", (team_id,))
        db.commit()
        return True
    except Exception as e:
        print(f"Error deleting team: {e}")
        return False
    finally:
        db.close()

def delete_player(player_id):
    db = get_db()
    cursor = db.cursor()

    # [Optional] Remove player from teams first (if you want to enforce this)
    cursor.execute("DELETE FROM team_members WHERE player_id = ?", (player_id,))

    # Delete player's game results
    cursor.execute("DELETE FROM game_results WHERE player_id = ?", (player_id,))

    # Delete the player
    cursor.execute("DELETE FROM players WHERE id = ?", (player_id,))

    db.commit()
    db.close()
        
def get_all_teams():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()

    # Convert sqlite3.Row objects to dictionaries
    team_dicts = []
    for team in teams:
        team_dict = dict(team)  # Convert to a dictionary
        team_id = team_dict['id']
        cursor.execute("""
            SELECT p.id, p.player_number
            FROM players p
            JOIN team_members tm ON p.id = tm.player_id
            WHERE tm.team_id = ?
        """, (team_id,))
        members = cursor.fetchall()
        team_dict['members'] = members  # Now you can assign the members
        team_dicts.append(team_dict)

    db.close()
    return team_dicts  # Return the list of dictionaries

def get_all_game_results():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM game_results")
    results = cursor.fetchall()
    db.close()
    return results

def is_player_eliminated(player_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM game_results WHERE player_id = ? AND result = 'eliminated'", (player_id,))
    result = cursor.fetchone()
    db.close()
    return result is not None

def get_team_id_by_name(game_name, team_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM teams WHERE game_name = ? AND team_name = ?", (game_name, team_name))
    team = cursor.fetchone()

   

    db.close()
    return team['id'] if team else None

def search_players_by_number(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, player_number, name FROM players WHERE player_number LIKE ?", ('%' + query + '%',))
    players = [{'id': row[0], 'player_number': row[1], 'name': row[2]} for row in cursor.fetchall()]
    conn.close()
    return players