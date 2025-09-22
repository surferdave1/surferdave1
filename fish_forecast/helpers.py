import requests
import sqlite3

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def air_temp(temp_f):
    #todo!
    return air_temp



def get_weather(lat, lng, weather_api_key):
    url = "http://api.weatherapi.com/v1/history.json"
    params = {
        "key": weather_api_key,
        "q": f"{lat},{lng}"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Example: extract temperature and condition
                #  Log the full response for debugging
        print("Full WeatherAPI response:")
        print(data)

        forecast_days = data.get("forecast", {}).get("forecastday", [])[0]
        
        if not forecast_days:
                    print("No forecast data available.")
                    return None

        day_info = forecast_days[0].get("day", {})
        condition = day_info.get("condition", {}).get("text", "Unknown")

    
        print(f"Location: {lat}, {lng}")
        print(f"Condition: {condition}")
        print(f"Avg Temp (°F): {day_info.get('avgtemp_f')}")
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None


def wind_speed(wind_mph):
    #todo!
    return wind_speed       

def pressure_trend(trend):
    #todo!
    return pressure_trend

def moon_phase(phase):
    #todo!
    # using solunar.org API
    # https://solunar.org/api.html
    # Example: https://solunar.org/solunar/api?lat=34.0522&lon=-118.2437&date=2023-10-01
    # You would replace lat, lon, and date with actual values
    # The API returns JSON data
    # You would parse the JSON to extract the moon phase information
    # For simplicity, let's assume the function receives the moon phase directly        
    # Possible values: "new", "first quarter", "full", "last quarter", etc.
    # determine latitude and longitude from user profile or input
    # determine current date
    # make API request and parse response
    # return the moon phase
    return moon_phase

def time_of_day(tod):
    #todo!
    return time_of_day

def season(season):
    #todo!
    return season

def get_db_connection():
     conn = sqlite3.connect("fish_forecast.db")
     conn.row_factory = sqlite3.Row
     return conn