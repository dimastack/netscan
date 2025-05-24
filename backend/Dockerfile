# Use a Python 3.13 base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install ping (iputils-ping) and clean up
RUN apt-get update && \
    apt-get install -y iputils-ping traceroute mtr-tiny && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file, Makefile, and alembic.ini to the container /app directory
COPY requirements.txt alembic.ini Makefile /app/

# Install dependencies globally (in the container's system Python environment)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend app code into the container
COPY netscan_app /app/netscan_app

# Set the environment variable to use Flask's built-in server in development mode
ENV FLASK_APP=netscan_app/main.py
ENV FLASK_ENV=development

# Expose the port that the Flask app will run on
EXPOSE 5001

# Run the application
# CMD ["python", "-m", "netscan_app.main"]
CMD ["gunicorn", "-b", "0.0.0.0:5001", "netscan_app.main:app", "--workers=4", "--threads=2"]

