from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# Database configuration
DATABASE_PATH = os.environ.get('DATABASE_PATH', '/data/blog.db')

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the posts table"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'blog-api'}), 200

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all blog posts"""
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    
    posts_list = []
    for post in posts:
        posts_list.append({
            'id': post['id'],
            'title': post['title'],
            'content': post['content'],
            'author': post['author'],
            'created_at': post['created_at'],
            'updated_at': post['updated_at']
        })
    
    return jsonify({'posts': posts_list}), 200

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific blog post by ID"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    
    if post is None:
        return jsonify({'error': 'Post not found'}), 404
    
    return jsonify({
        'id': post['id'],
        'title': post['title'],
        'content': post['content'],
        'author': post['author'],
        'created_at': post['created_at'],
        'updated_at': post['updated_at']
    }), 200

@app.route('/api/posts', methods=['POST'])
def create_post():
    """Create a new blog post"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content') or not data.get('author'):
        return jsonify({'error': 'Missing required fields: title, content, author'}), 400
    
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
        (data['title'], data['content'], data['author'])
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'message': 'Post created successfully',
        'id': post_id
    }), 201

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update an existing blog post"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    
    if post is None:
        conn.close()
        return jsonify({'error': 'Post not found'}), 404
    
    title = data.get('title', post['title'])
    content = data.get('content', post['content'])
    author = data.get('author', post['author'])
    
    conn.execute(
        'UPDATE posts SET title = ?, content = ?, author = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (title, content, author, post_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Post updated successfully'}), 200

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a blog post"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    
    if post is None:
        conn.close()
        return jsonify({'error': 'Post not found'}), 404
    
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Post deleted successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
