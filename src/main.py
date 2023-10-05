from flask import Flask, render_template
from models import BaseModel
from db import DataBase


app = Flask(__name__)
db = DataBase(database_url="sqlite:///mydatabase.db", base_model=BaseModel)
db.delete_all_in_all_tables()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")
