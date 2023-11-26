# IKT222  Software security
This repository contains a Flask application used to demostrate security vulnerabilities 
as part of the course IKT222 at University of Agder.

The application is a blog where users can register and post blogposts.

## Disclaimer: This repository is ment to demonstrate security vulnerabilities as part of an education program. Do not attempt to exploit the vulnerabilities demonstrated here in any malicious way.

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

Creating a .env file
```bash
python -c 'import secrets; print("APP_SECRET="+secrets.token_hex())' > .env
```
This will generate a random app secret in a .env file, keep it secret.

## Runing locally
Run application locally by running command from project root
```bash
flask --app src/main.py --debug run
```
Application should now be running at http://localhost:5000/

Running the auth server locally
```bash
flask --app src/oauth/server.py --debug run --port 5001
```
Oauth server should now be running at http://localhost:5001/

## Docker
Build and run application in docker image by running commands from project root
```bash
docker build -t ikt222-flask-image . -f ./Docker/Dockerfile
docker run -d --name ikt222-flask-app -p 8000:8000 ikt222-flask-image
```

Application should now be running at http://localhost:8000/