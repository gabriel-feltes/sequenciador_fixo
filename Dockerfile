# Use the official Python image as the base image
FROM python:3.11-slim

# Set environment variables to prevent Python from buffering logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /backend

# Copy the requirements file into the container
COPY backend/requirements.txt /backend/requirements.txt

# Install system dependencies and Python dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the backend application files into the container
COPY backend /backend

# Copy the frontend application files into the container
COPY frontend /backend/frontend

# Expose the port the app runs on
EXPOSE 5000

# Set the command to run the Flask application
CMD ["python", "server.py"]