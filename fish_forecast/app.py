import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, get_db_connection, login_required, get_weather, air_temp, wind_speed, pressure_trend, moon_phase, time_of_day, season
from forecast import bass_fishing_quality
import requests

weather_api_key = "12c96143c1c24894836214843252908"

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite3 connection
#conn = sqlite3.connect("fish_forecast.db", check_same_thread=False)
#conn.row_factory = sqlite3.Row
#db = conn.cursor()

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
   
    return render_template("forecast.html" )

@app.route("/forecast")
def forecast():
    user_id = session.get("user_id")
    if not user_id:
        return "User not logged in", 401

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT latitude, longitude, timestamp
            FROM user_locations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (user_id,))
    result = cursor.fetchone()

    if not result:
        # No location settings found — show fallback message
        return render_template("forecast.html", no_settings=True)

    lat, lng, _ = result
    print(f"User {user_id} forecast request for lat ={lat}, lng={lng}")

    weather_data = get_weather(lat, lng, weather_api_key)
    if not weather_data:
        return render_template("forecast.html", error="Weather data unavailable")

    forecast = weather_data["forecast"]["forecastday"][0]["day"]
    condition = forecast["condition"]["text"]
    avgtemp_f = forecast["avgtemp_f"]
    local_date = weather_data["location"]["localtime"].split(" ")[0]

    return render_template("forecast.html", lat=lat, lng=lng, date=local_date,
                           condition=condition, avgtemp_f=avgtemp_f)

@app.route("/about")
@login_required
def about():
    user_id = session["user_id"]
   
    return render_template("about.html" )
    #TODO!


@app.route("/settings", methods=["GET", "POST"])
def settings():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    return render_template("settings.html")
    
@app.route("/save_settings", methods=["POST"])
@login_required
def save_settings():
    user_id = session["user_id"]
    data = request.get_json()

    lat = data.get("lat")
    lng = data.get("lng")
    date = data.get("date")

    if not lat or not lng or not date:
        return jsonify({"error": "All fields are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_locations (user_id, latitude, longitude, timestamp)
            VALUES (?, ?, ?, ?)
        """, (user_id, lat, lng, date))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database error:", e)
        return jsonify({"error": "Database error"}), 500

    return jsonify({"message": "Settings saved successfully!"})

@app.route("/contact")
@login_required
def contact():
    user_id = session["user_id"]
   #todo
    return render_template("contact.html" )

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = cursor.fetchall()
        conn.close()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 400)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        if not password or not confirmation:
            return apology("must provide and confirm password", 400)
        if password != confirmation:
            return apology("Passwords do not match", 400)
        # debugging to check log registration attempt
        print(f"attempting to register user: {username}")
        hash_pw = generate_password_hash(password)
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
                conn.commit()
        except sqlite3.IntegrityError:
            return apology("Username already exists", 400)
        return redirect("/")
    return render_template("register.html")

