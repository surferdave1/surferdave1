import requests
import sqlite3

from flask import redirect, render_template, session
from functools import wraps
from datetime import datetime
from pprint import pprint

# apology from the CS50 finance project
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

# login_required from the CS50 finance project
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

# get_weather was created with assistance from co-pilot
def get_weather(location, weather_api_key, date=None):
    # Use today's date
    date = datetime.today().strftime('%Y-%m-%d')
    
    url = "http://api.weatherapi.com/v1/history.json"
    params = {
        "key": weather_api_key,
        "q": f"{location}",
        "dt": date
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Weather API request failed: {e}")
        return None
    except ValueError:
        print("Invalid JSON response")
        return None

    try:
        forecast_day = data.get("forecast", {}).get("forecastday", [])[0]
        location = data.get("location", {}).get("name", "Unknown")
        region = data.get("location", {}).get("region", "Unknown")
        country = data.get("location", {}).get("country", "Unknown")    
        day_info = forecast_day.get("day", {})
        condition = day_info.get("condition", {}).get("text", "Unknown")
        avgtemp_f = day_info.get("avgtemp_f", "N/A")
        maxwind_mph = day_info.get("maxwind_mph", "N/A")
        localtime = data.get("location", {}).get("localtime", "Unknown")
        current_hour_24hr = int(localtime.split()[1].split(':')[0])
        current_time_24hr = localtime.split()[1]
        hour = forecast_day.get("hour", [])[current_hour_24hr]
        pressure_in = hour.get("pressure_in", "N/A")
        def avg_morning_pressure(pressure_in):
            total_pressure = 0
            count = 0
            for h in forecast_day.get("hour", []):
                hour_time = h.get("time", "")
                if hour_time and int(hour_time.split()[1].split(':')[0]) < 12:
                    total_pressure += h.get("pressure_in", 0)
                    count += 1
            return total_pressure / count if count > 0 else 0
        avg_morning_pressure_in = avg_morning_pressure(pressure_in)
        print(f"Average morning pressure: {avg_morning_pressure_in}")
        def avg_afternoon_pressure(pressure_in):
            total_pressure = 0
            count = 0
            for h in forecast_day.get("hour", []):
                hour_time = h.get("time", "")
                if hour_time and int(hour_time.split()[1].split(':')[0]) >= 12:
                    total_pressure += h.get("pressure_in", 0)
                    count += 1
            return total_pressure / count if count > 0 else 0
        avg_afternoon_pressure_in = avg_afternoon_pressure(pressure_in)
        print(f"Average afternoon pressure: {avg_afternoon_pressure_in}")   
        def max_pressure(pressure_in):
            # start with hour 0
            # find pressure. 
            # Loop through all hours to find max pressure
            max_p = 0
            for h in forecast_day.get("hour", []):
                p = h.get("pressure_in", 0)
                if p > max_p:
                    max_p = p
                    high_hour = h.get("time", "")                    
            print(f"Max pressure for the day: {max_p}, Hour: {high_hour}")
            return max_p
        max_pressure_in_output = max_pressure(pressure_in)
        def min_pressure(pressure_in):            
            min_p = 1000
            for h in forecast_day.get("hour", []):
                p = h.get("pressure_in", 1000)
                if p < min_p:
                    min_p = p
                    low_hour = h.get("time", "")                    
            print(f"Min pressure for the day: {min_p}, Hour: {low_hour}")
            return min_p
        min_pressure_in_output = min_pressure(pressure_in)
        def pressure_trend(avg_morning_pressure_in, avg_afternoon_pressure_in):
            if abs(avg_afternoon_pressure_in - avg_morning_pressure_in) < 0.03:
                return "steady"
            elif avg_afternoon_pressure_in < avg_morning_pressure_in:
                return "falling"
            elif avg_afternoon_pressure_in > avg_morning_pressure_in:
                return "rising"
            else:
                return "unclear"
        pressure_trend_output = pressure_trend(avg_morning_pressure_in, avg_afternoon_pressure_in)
        print(f"Pressure trend for the day: {pressure_trend_output}")
        wind_mph = hour.get("wind_mph", "N/A")
        humidity = hour.get("humidity", "N/A")
        astro = forecast_day.get("astro", {})
        moon_phase = astro.get("moon_phase", "N/A")
        sunrise = astro.get("sunrise", "N/A")
        sunrise_time_24hr = (sunrise.split(' ')[0])
        sunset = astro.get("sunset", "N/A")

        def convert_pm_to_24hr(time_str):
            time_str = time_str.replace(" AM", "").replace(" PM", "")
            hour, minute = map(int, time_str.split(':'))
            if "PM" in sunset and hour != 12:
                hour += 12
            return f"{hour:02d}:{minute:02d}"
        sunset_time_24hr = convert_pm_to_24hr(sunset)
        moonrise = astro.get("moonrise", "N/A")
        moonset = astro.get("moonset", "N/A") 
        return date, region, country, condition, avgtemp_f, maxwind_mph, localtime, pressure_in, wind_mph, humidity, moon_phase, sunrise, sunset, moonrise, moonset, current_hour_24hr,current_time_24hr, sunset_time_24hr, sunrise_time_24hr, pressure_trend_output, max_pressure_in_output, min_pressure_in_output, avg_morning_pressure_in, avg_afternoon_pressure_in
    except (IndexError, KeyError) as e:
        print(f"Error parsing forecast data: {e}")
        return None

#get_db_connection was created with assistance from co-pilot
def get_db_connection():
     conn = sqlite3.connect("fish_forecast.db")
     conn.row_factory = sqlite3.Row
     return conn

