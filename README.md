# A RESTful Blog API with Flask, SQLite DB, Docker Network + Volume

A RESTful blog API built with Flask, using SQLite database stored in a Docker volume, and running on a custom Docker network.

## Features

- **Flask REST API** with full CRUD operations for blog posts
- **SQLite database** for data persistence
- **Docker volume** for database storage
- **Custom Docker network** for container networking
- Health check endpoint
- Automatic database initialization

## Project Structure

```
.
├── app.py                 # Flask application with API endpoints
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Docker build exclusions
└── README.md            # This file
```

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Clone or navigate to the project directory**

2. **Build and start the containers**:
   ```bash
   docker-compose up --build
   ```

3. **Access the API**:
   - API will be available at: `http://localhost:5000`
   - Health check: `http://localhost:5000/health`

4. **Stop the containers**:
   ```bash
   docker-compose down
   ```

5. **Remove volumes (if you want to delete the database)**:
   ```bash
   docker-compose down -v
   ```

## API Endpoints

### Health Check
- **GET** `/health`
  - Returns API health status

### Get All Posts
- **GET** `/api/posts`
  - Returns all blog posts

### Get Single Post
- **GET** `/api/posts/<post_id>`
  - Returns a specific post by ID

### Create Post
- **POST** `/api/posts`
  - Body:
    ```json
    {
      "title": "Post Title",
      "content": "Post content here...",
      "author": "Author Name"
    }
    ```

### Update Post
- **PUT** `/api/posts/<post_id>`
  - Body (all fields optional):
    ```json
    {
      "title": "Updated Title",
      "content": "Updated content...",
      "author": "Updated Author"
    }
    ```

### Delete Post
- **DELETE** `/api/posts/<post_id>`
  - Deletes a specific post

## Testing the API with curl

### Create a post:
```bash
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Kyushu Chronicles",
    "content": "There will be blood, and it will be red in color...",
    "author": "Shinobi Hasegawa"
  }'
```

### Get all posts:
```bash
curl http://localhost:5000/api/posts
```

### Get a specific post:
```bash
curl http://localhost:5000/api/posts/1
```

### Update a post:
```bash
curl -X PUT http://localhost:5000/api/posts/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Blog Post Title"
  }'
```

### Delete a post:
```bash
curl -X DELETE http://localhost:5000/api/posts/1
```

## Docker Architecture

### Custom Network
- **Network Name**: `blog-custom-network`
- **Driver**: bridge
- Isolates the blog service on a dedicated network

### Volume
- **Volume Name**: `blog-database-volume`
- **Mount Point**: `/data` inside the container
- **Database File**: `/data/blog.db`
- Persists SQLite database across container restarts

### Container
- **Name**: `blog-flask-api`
- **Port Mapping**: `5000:5000`
- **Restart Policy**: `unless-stopped`

## Database Schema

The SQLite database contains a `posts` table with the following structure:

| Column     | Type      | Description                    |
|------------|-----------|--------------------------------|
| id         | INTEGER   | Primary key (auto-increment)   |
| title      | TEXT      | Post title                     |
| content    | TEXT      | Post content                   |
| author     | TEXT      | Post author                    |
| created_at | TIMESTAMP | Creation timestamp             |
| updated_at | TIMESTAMP | Last update timestamp          |

## Environment Variables

- `DATABASE_PATH`: Path to SQLite database file (default: `/data/blog.db`)

## Development

To run locally without Docker:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. The API will be available at `http://localhost:5000`

## Docker Commands Reference

### View running containers:
```bash
docker ps
```

### View logs:
```bash
docker-compose logs -f
```

### View networks:
```bash
docker network ls
docker network inspect blog-custom-network
```

### View volumes:
```bash
docker volume ls
docker volume inspect blog-database-volume
```

### Execute commands in container:
```bash
docker exec -it blog-flask-api bash
```

### Rebuild without cache:
```bash
docker-compose build --no-cache
docker-compose up
```
