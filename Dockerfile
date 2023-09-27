# Base image for the container
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt .

# Install the required dependencies
RUN pip install -r requirements.txt

COPY . .

# Expose the port 5000
EXPOSE 5000

# Run the Flask app with Gunicorn
CMD gunicorn app:app --bind 0.0.0.0:5000