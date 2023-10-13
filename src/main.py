from flask import Flask, render_template, request
import models
from db import DataBase


app = Flask(__name__)
db = DataBase(database_url="sqlite:///mydatabase.db", base_model=models.BaseModel)
db.delete_all_in_all_tables()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/post", methods=["Get", "Post"])
def post():
    if request.method == "POST":
        # Create a new post
        post = models.Post(
            title=request.form["title"],
            content=request.form["content"]
        )
        db.create(post);
        return render_template("index.html", posts = [post for post in db.query(models.Post).all()])
    return render_template("post.html")

@app.route("/about")
def about():
    return render_template("about.html")
