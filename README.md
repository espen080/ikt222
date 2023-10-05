# IKT222  Software security
This repository contains a Flask application used to demostrate security vulnerabilities 
as part of the course IKT222 at University of Agder.

The application is a blog where users can register and post blogposts.

## Installation
Create virtual environment
```bash
py -3 -m venv .venv
cd .venv/Scripts
. activate
cd ../..
```

Install requirements
```bash
pip install -r requirements.txt
```

## Runing locally
Run application locally by running command from project root
```bash
flask --app src/main.py run
```

## Docker
Build and run application in docker image by running commands from project root
```bash
docker build -t ikt222-flask-image . -f ./Docker/Dockerfile
docker run -d --name ikt222-flask-app -p 8000:8000 ikt222-flask-image
```

Application should now be running at http://localhost:8000/