import os
from flask import Flask, render_template, redirect, url_for, request, session, g, flash, make_response, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import models
import auth
from db import DataBase
import datetime

load_dotenv()

app_secret = os.getenv("APP_SECRET")

app = Flask(__name__, static_url_path='/static')
CORS(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["2000 per day", "500 per hour", "3 per second"],
    storage_uri="memory://",
)
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_TIME = 1 # minutes

@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
            jsonify(error=f"ratelimit exceeded {e.description}")
            , 429
    )

csp = {
    'default-src': ['\'self\''],
    'script-src': [
        '\'self\'',
        'https://stackpath.bootstrapcdn.com', 
        'https://code.jquery.com',
        'https://cdn.jsdelivr.net',
    ],
    'style-src': [
        '\'self\'',
        'https://stackpath.bootstrapcdn.com',
    ],
    }
Talisman(app, content_security_policy=csp)
app.secret_key = app_secret

db = DataBase(database_url="sqlite:///secureblog.db", base_model=models.BaseModel)


@app.route("/")
@auth.authenticate
def index():
    return render_template("index.html", posts = [post for post in db.query(models.Post).all()])

@app.route("/post", methods=["Get", "Post"])
@auth.authenticate
def create_post():
    if request.method == "POST":
        # Create a new post
        post = models.Post(
            title=request.form["title"],
            content=request.form["content"],
            created_at=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            user_id=g.user.id
        )
        db.create(post);
        return redirect(url_for("index"))
    return render_template("create_post.html")

@app.route("/post/<int:post_id>")
@auth.authenticate
def view_post(post_id):
    post = db.query(models.Post).filter_by(id=post_id).first()
    print(post.user.first_name)
    return render_template("view_post.html", post=post)

@app.route("/post/<int:post_id>/edit", methods=["Get", "Post"])
@auth.authenticate
def edit_post(post_id):
    if g.user.id != db.query(models.Post).filter_by(id=post_id).first().user_id:
        flash("You are not authorized to edit this post.")
        return redirect(url_for("index"))
    if request.method == "POST":
        # Update post
        db.update(
            models.Post, 
            {"id": post_id}, 
            {
                "title": request.form["title"], 
                "content": request.form["content"], 
                "modified_at": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            }
        )
        return redirect(url_for("index"))
    post = db.query(models.Post).filter_by(id=post_id).first()
    return render_template("edit_post.html", post=post)

@app.route("/about")
@auth.authenticate
def about():
    return render_template("about.html")

@app.route("/hacker-website", methods=["Post"])
def hacker_website():
    print(request.get_json())
    return "Got it"

@app.route("/register", methods=["Get", "Post"])
@limiter.limit("5 per day")
def register():
    if request.method == "POST":
        if db.query(models.User).filter_by(email=request.form["email"]).first() is not None:
            flash("Email already in use.")
            return redirect(url_for("register"))
        if request.form["password"] != request.form["confirm_password"]:
            flash("Passwords do not match.")
            return redirect(url_for("register"))
        # Create a new user
        user = models.User(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            email=request.form["email"],
            password=auth.hash_password(request.form["password"])
        )
        db.create(user)
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["Get", "Post"])
@limiter.limit("20/minute", override_defaults=False)
def login():
    if request.method == "GET":
        return render_template("login.html")

    # Check if the user exists
    user = db.query(models.User).filter_by(email=request.form["email"]).first()
    if user is None:
        flash("Incorrect email or password.")
        return redirect(url_for("login"))
    
    # Check if the user is locked out
    if user.locked_to is not None and user.locked_to > datetime.datetime.now():
        flash("Your account is locked. Please try again later.")
        return redirect(url_for("login"))
    
    # Lock the user out if they have failed to login too many times
    if len(user.logins) >= MAX_LOGIN_ATTEMPTS and user.locked_to is None:
        user.locked_to = datetime.datetime.now() + datetime.timedelta(minutes=LOCKOUT_TIME)
        db.update(models.User, {"id": user.id}, {"locked_to": user.locked_to})
        flash("Your account is locked. Please try again later.")
        return redirect(url_for("login"))
        
    # Check if the password is correct
    if not auth.verify_password(request.form["password"], user.password):
        return save_failed_login_attempt(request, user.id)

    # Log the user in
    session["user_id"] = user.id
    db.delete(models.Login, user_id=user.id)
    db.update(models.User, {"id": user.id}, {"locked_to": None})
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = db.query(models.User).filter_by(id=user_id).first()

def save_failed_login_attempt(request, user_id):
    # Save request data
    login_request = models.Login(
        user_id=user_id,
        ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
        user_agent=request.user_agent.string,
        timestamp=datetime.datetime.now()
    )
    db.create(login_request)
    flash("Incorrect email or password.")
    return redirect(url_for("login"))
