# Use a Python 3.8 base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies globally (in the container's system Python environment)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend application to the container
COPY . /app/

# Set the environment variable to use Flask's built-in server in development mode
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expose the port that the Flask app will run on
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]
