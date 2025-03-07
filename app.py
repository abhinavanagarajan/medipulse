from flask import Flask, send_from_directory, render_template
import subprocess
import os
import sys
from flask_cors import CORS

app = Flask(__name__, 
           static_folder='mediplus-lite',
           template_folder='mediplus-lite')
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GAMES_DIR = os.path.join(BASE_DIR, 'games')

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return send_from_directory('mediplus-lite', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('mediplus-lite', filename)

@app.route('/mydata')
def mydata():
    return send_from_directory('mediplus-lite', 'myData.html')

@app.route('/relax.html')
def relax():
    return send_from_directory('mediplus-lite', 'relax.html')

@app.route('/blog-single.html')
def blog():
    return send_from_directory('mediplus-lite', 'blog-single.html')

@app.route('/contact.html')
def contact():
    return send_from_directory('mediplus-lite', 'contact.html')

@app.route('/games/<game>')
def launch_game(game):
    game_files = {
        'doodle': 'doodle.py',
        'puzzle': 'puzzle.py',
        'rhythm': 'rhythm.py',
        'breathing': 'breathing.py',
        'music': 'particlemusic.py'  # Add this line
    }
    
    if game in game_files:
        try:
            game_path = os.path.join(GAMES_DIR, game_files[game])
            if os.path.exists(game_path):
                subprocess.Popen(
                    [sys.executable, game_path], 
                    cwd=GAMES_DIR,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                return "Game launched", 200
            return "Game not found", 404
        except Exception as e:
            print(f"Error launching game: {e}")
            return str(e), 500
    return "Invalid game", 400

if __name__ == '__main__':
    print(f"Base directory: {BASE_DIR}")
    print(f"Games directory: {GAMES_DIR}")
    os.makedirs(GAMES_DIR, exist_ok=True)
    app.run(debug=True, port=5000)
