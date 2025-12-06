from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE_PATH = os.environ.get('DATABASE_PATH', '/data/blog.db')

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

# Initializing the database upon starting the serving application
init_db()

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'blog-api'}

@app.route('/api/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
        return {'posts': [dict(row) for row in rows]}
    
    data = request.get_json()
    if not all(k in data for k in ['title', 'content', 'author']):
        return {'error': 'Missing required fields: title, content, author'}, 400
    
    with get_db() as conn:
        cursor = conn.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                            (data['title'], data['content'], data['author']))
        conn.commit()
    return {'message': 'Post created', 'id': cursor.lastrowid}, 201

@app.route('/api/posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post(post_id):
    with get_db() as conn:
        row = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
        
        if not row:
            return {'error': 'Post not found'}, 404
        
        if request.method == 'GET':
            return dict(row)
        
        if request.method == 'DELETE':
            conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
            conn.commit()
            return {'message': 'Post deleted'}
        
        data = request.get_json() or {}
        conn.execute('''UPDATE posts SET title = ?, content = ?, author = ?, 
                       updated_at = CURRENT_TIMESTAMP WHERE id = ?''',
                    (data.get('title', row['title']), 
                     data.get('content', row['content']),
                     data.get('author', row['author']), post_id))
        conn.commit()
        return {'message': 'Post updated'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
