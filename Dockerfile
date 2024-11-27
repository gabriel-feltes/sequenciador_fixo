# Use the official Python image as the base image
FROM python:3.11-slim

# Set environment variables to prevent Python from buffering logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /sequenciador_fixo

# Copy the backend and frontend files
COPY backend /sequenciador_fixo/backend
COPY frontend /sequenciador_fixo/frontend

# Set the working directory to the backend
WORKDIR /sequenciador_fixo/backend

# Install Python dependencies
COPY backend/requirements.txt /sequenciador_fixo/backend/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Set the command to run the application
CMD ["python", "server.py"]
