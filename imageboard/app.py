from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    boards = [name for name in os.listdir('boards') if os.path.isdir(os.path.join('boards', name))]
    return render_template('index.html', boards=boards)

@app.route('/<board>/')
def board(board):
    board_folder = f'boards/{board}'
    board_file = f'{board_folder}/board.json'
    board_name_file = f'{board_folder}/board_name.txt'

    # Load posts from the board JSON file
    if os.path.exists(board_file):
        with open(board_file, 'r') as f:
            posts = json.load(f)
    else:
        posts = []

    # Load the board name from the text file if it exists
    if os.path.exists(board_name_file):
        with open(board_name_file, 'r') as f:
            board_name = f.read().strip()
    else:
        board_name = board  # Fallback to just the board identifier if no name file exists

    # Display all posts (newest first)
    return render_template('board.html', board=board, posts=posts[::-1], board_name=board_name)  # Reverse the posts to show the newest first

@app.route('/<board>/', methods=['POST'])
def create_thread(board):
    board_folder = f'boards/{board}'
    board_file = f'{board_folder}/board.json'

    # Ensure the board folder exists
    os.makedirs(board_folder, exist_ok=True)

    # Load existing posts or initialize a new list
    if os.path.exists(board_file):
        with open(board_file, 'r') as f:
            posts = json.load(f)
    else:
        posts = []

    # Create a new post
    new_post = {
        'name': request.form.get('name', 'Anonymous'),
        'title': request.form.get('title', ''),
        'text': request.form.get('text', ''),
        'image': request.files['image'].filename if 'image' in request.files and request.files['image'].filename else None
    }

    # Save the image if it exists
    if 'image' in request.files and request.files['image'].filename:
        image_file_path = os.path.join('static/uploads', request.files['image'].filename)
        request.files['image'].save(image_file_path)

    # Insert the new post at the beginning of the list
    posts.insert(0, new_post)  # Add new post at the top

    # Save the updated posts back to the JSON file
    with open(board_file, 'w') as f:
        json.dump(posts, f)

    return redirect(url_for('board', board=board))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
