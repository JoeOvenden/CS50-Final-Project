from flask import Flask, render_template

# Configure application
app = Flask(__name__)

@app.route("/gravity")
def gravity():
    return render_template("gravity.html")

@app.route("/newtons-law")
def newtons_law():
    return render_template("newtons-law.html")

@app.route("/drag-and-friction")
def drag_and_friction():
    return render_template("drag-and-friction.html")

@app.route("/conservation")
def conservation():
    return render_template("conservation.html")

@app.route("/buoyancy")
def buoyancy():
    return render_template("buoyancy.html")

@app.route("/simulator")
def simulator():
    return render_template("simulator.html")

@app.route("/asteroids")
def asteroids():
    return render_template("asteroids.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
def index():
    return render_template("index.html")
