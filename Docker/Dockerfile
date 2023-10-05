# syntax=docker/dockerfile:1

FROM python:3.11

# Set working directory for container
WORKDIR /app

# Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy app source
Copy ./src /app/src

ENTRYPOINT gunicorn --chdir src main:app -w 2 --threads 2 -b 0.0.0.0:8000

