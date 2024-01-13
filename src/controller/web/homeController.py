from flask import render_template

from app import app
from src.utils.httpMethod import HttpMethod


@app.route('/', methods=[HttpMethod.GET])
def view_index():
    return render_template("index.html")


@app.route('/providers', methods=[HttpMethod.GET])
def view_provider():
    return render_template("providers.html")


@app.route('/rates', methods=[HttpMethod.GET])
def view_rates():
    return render_template("rates.html")


@app.route('/trucks', methods=[HttpMethod.GET])
def view_trucks():
    return render_template("trucks.html")
