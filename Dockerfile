FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create volume mount point for database
RUN mkdir -p /data

# Expose Flask port
EXPOSE 5000

# Set environment variable for database path
ENV DATABASE_PATH=/data/blog.db

# Run the Flask application
CMD ["python", "app.py"]
