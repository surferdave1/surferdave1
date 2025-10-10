from __future__ import print_function
import time
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, get_db_connection, login_required, get_weather
from bass import forecast_bass
from carp import forecast_carp
from catfish import forecast_catfish
from crappie import forecast_crappie
from panfish import forecast_panfish
from pike import forecast_pike
from muskie import forecast_muskie
from salmon import forecast_salmon
from trout import forecast_trout
from walleye import forecast_walleye
import requests
from flask import abort

weather_api_key = "12c96143c1c24894836214843252908"
# Configure API key authorization: ApiKeyAuth
configuration = weatherapi.Configuration()
configuration.api_key['key'] = '12c96143c1c24894836214843252908'


# Configure application
app = Flask(__name__)

# the following section was created with co-pilot, and customized by me to enable debug mode
# Ensure templates reload when changed during development
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
# Disable static file caching in development so CSS/JS changes show up
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
date = datetime.today().strftime('%Y-%m-%d')
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Helper available in templates to return a current timestamp for cache-busting in development
app.jinja_env.globals['now_ts'] = lambda: int(time.time())


# after_request was created with co-pilot to enable debug mode
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
@login_required

def weather_forecast():

    return render_template("forecast.html", )

# /location_change was created with asssistance from co-pilot
@app.route("/location_change", methods=["GET","POST"])
@login_required
def location_change():
    # Ensure POST data (location) is JSON
    if not request.is_json:
        return jsonify({"error": "Invalid input, JSON expected"}), 400

    data = request.get_json()
    location = data.get("location")
    fish_species = data.get("fish_species")
    print(f"Location: {location}, Fish Species: {fish_species}")

    if not location:
        return jsonify({"error": "Location is required"}), 400

    
    weather_data = get_weather(location, weather_api_key)
    if not weather_data:
        return jsonify({"error": "Failed to fetch weather data"}), 502  
    # unpack the returned values
    
    keys = [
        "date", "region", "country", "condition", "avgtemp_f", "maxwind_mph", "localtime",
        "pressure_in", "wind_mph", "humidity", "moon_phase", "sunrise", "sunset",
        "moonrise", "moonset", "current_hour_24hr", "current_time_24hr",
        "sunset_time_24hr", "sunrise_time_24hr", "pressure_trend_output",
        "max_pressure_in_output", "min_pressure_in_output",
        "avg_morning_pressure_in", "avg_afternoon_pressure_in"
    ]

    # Combine keys and values into a dictionary
    data = dict(zip(keys, weather_data))

    #(date, region, country, condition, avgtemp_f, maxwind_mph, localtime, pressure_in, wind_mph, humidity, moon_phase, sunrise, sunset, moonrise, moonset, current_hour_24hr,current_time_24hr, sunset_time_24hr, sunrise_time_24hr, pressure_trend_output, max_pressure_in_output, min_pressure_in_output, avg_morning_pressure_in, avg_afternoon_pressure_in) = weather_data
    #print(f"Weather Data - Date: {date}, Region: {region}, Country: {country}, Condition: {condition}, Avg Temp: {avgtemp_f}, Max Wind: {maxwind_mph}, Local Time: {localtime}, Pressure: {pressure_in}, Wind: {wind_mph}, Humidity: {humidity}, Moon Phase: {moon_phase}, Sunrise: {sunrise}, Sunset: {sunset}, Moonrise: {moonrise}, Moonset: {moonset}, Current Hour: {current_hour_24hr}, Current Time: {current_time_24hr}, Sunset Time 24hr: {sunset_time_24hr}, Sunrise Time 24hr: {sunrise_time_24hr}, Pressure Trend: {pressure_trend_output}, Max Pressure: {max_pressure_in_output}, Min Pressure: {min_pressure_in_output}, Avg Morning Pressure: {avg_morning_pressure_in}, Avg Afternoon Pressure: {avg_afternoon_pressure_in}")
    print(f"Weather Data - {data}")
    # fish forecast
    current_score = None
    current_rating = None
    #forecast_name = f"forecast_{fish_species.lower()}(date, avgtemp_f, condition, maxwind_mph,moon_phase, current_time_24hr, season, sunset_time_24hr, sunrise_time_24hr, pressure_trend_output)"
    
    forecast_func = globals().get(f"forecast_{fish_species.lower()}")

    
    current_score, current_rating, dawn_dusk_rating, morning_evening_rating = forecast_func(data)
        
    print(f"Current {fish_species} Forecast Score: {current_score}/100, Current Rating: {current_rating} ")
         
    print("Returning weather and forecast data to frontend")
    return jsonify({
        "date": data['date'],
        "region": data['region'],
        "country": data['country'],
        "condition": data['condition'],
        "avgtemp_f": data['avgtemp_f'],
        "maxwind_mph": data['maxwind_mph'],
        "localtime": data['localtime'],
        "pressure_in": data['pressure_in'],
        "wind_mph": data['wind_mph'],
        "humidity": data['humidity'],
        "moon_phase": data['moon_phase'],
        "sunrise": data['sunrise'],
        "sunset": data['sunset'],
        "moonrise": data['moonrise'],
        "moonset": data['moonset'],
        "current_hour_24hr": data['current_hour_24hr'],
        "current_time_24hr": data['current_time_24hr'],
        "sunset_time_24hr": data['sunset_time_24hr'],
        "sunrise_time_24hr": data['sunrise_time_24hr'],
        "pressure_trend_output": data['pressure_trend_output'],
        "max_pressure_in_output": data['max_pressure_in_output'],
        "min_pressure_in_output": data['min_pressure_in_output'],
        "avg_morning_pressure_in": data['avg_morning_pressure_in'],
        "avg_afternoon_pressure_in": data['avg_afternoon_pressure_in'],
        "fish_species": fish_species,
        # forecast results
        "current_score": current_score,
        "current_rating": current_rating,
        "dawn_dusk_rating": dawn_dusk_rating,
        "morning_evening_rating": morning_evening_rating
        
         })
    



    
@app.route("/about")
@login_required
def about():
    user_id = session["user_id"]
   
    return render_template("about.html" )
    

@app.route("/contact")
@login_required
def contact():
    user_id = session["user_id"]
   
    return render_template("contact.html" )

@app.route("/login", methods=["GET", "POST"])

# login was from CCS50 finance project
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


# /register was from CS50 finance project
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

