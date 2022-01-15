from flask import Flask,render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():

    mars_info = mongo.db.mars_info.find_one()

    return render_template("index.html", data=mars_info)

@app.route("/scrape")
def data_scrape():

    info = mongo.db.mars_info

    mars_data = scrape_mars.scrape()

    info.update({}, mars_data, upsert=True)
    return redirect("/")

# main
if __name__ == "__main__":
    app.run(debug = True)