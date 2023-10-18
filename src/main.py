from flask import Flask, render_template, redirect, url_for, request
import models
from db import DataBase


app = Flask(__name__, static_url_path='/static')
db = DataBase(database_url="sqlite:///mydatabase.db", base_model=models.BaseModel)
# db.delete_all_in_all_tables()


@app.route("/")
def index():
    return render_template("index.html", posts = [post for post in db.query(models.Post).all()])

@app.route("/post", methods=["Get", "Post"])
def create_post():
    if request.method == "POST":
        # Create a new post
        post = models.Post(
            title=request.form["title"],
            content=request.form["content"]
        )
        db.create(post);
        return redirect(url_for("index"))
    return render_template("create_post.html")

@app.route("/post/<int:post_id>")
def view_post(post_id):
    post = db.query(models.Post).filter_by(id=post_id).first()
    return render_template("view_post.html", post=post)



@app.route("/post/<int:post_id>/edit", methods=["Get", "Post"])
def edit_post(post_id):
    if request.method == "POST":
        # Update post
        db.update(
            models.Post, 
            {"id": post_id}, 
            {"title": request.form["title"], "content": request.form["content"]}
        )
        return redirect(url_for("index"))
    post = db.query(models.Post).filter_by(id=post_id).first()
    return render_template("edit_post.html", post=post)

@app.route("/about")
def about():
    return render_template("about.html")
