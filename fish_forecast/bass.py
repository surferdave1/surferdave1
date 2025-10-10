from datetime import datetime

# the following code was created with co-pilot, and customized by me

def forecast_bass(data):
    current_score = 0
    print(f"score: {current_score}")
    print(f"Input - Date: {data['date']}, Avg Temp: {data['avgtemp_f']}, Condition: {data['condition']}, Max Wind: {data['maxwind_mph']}, Moon Phase: {data['moon_phase']}, Current Time: {data['current_time_24hr']}, Sunset Time: {data['sunset_time_24hr']}, Sunrise Time: {data['sunrise_time_24hr']}")

    def season_from_date(date_str):
            month = int(date_str.split('-')[1])
            if month in [3, 4, 5]:
                return "spring"
            elif month in [6, 7, 8]:
                return "summer"
            elif month in [9, 10, 11]:
                return "fall"
            else:
                return "winter"
    season = season_from_date(data['date'])
    print(f"Determined season: {season}")
    # Temperature scoring (ideal range: 55–75°F)
    if season=="spring" and 50 <= data['avgtemp_f'] <= 70:
        current_score += 10
    elif season=="summer" and 70 <= data['avgtemp_f'] <= 85:
        current_score += 10
    elif season=="fall" and 50 <= data['avgtemp_f'] <= 65:
        current_score += 10   
    elif season=="winter" and 35 <= data['avgtemp_f'] <= 50:
        current_score += 10   
    else:
        current_score += 0
    print(f"Score after temperature: {current_score}"   )
    
    # Weather scoring
    # todo: find out all possible weather conditions from API
    def weather_condition_score(condition):
        condition = condition.lower()
        if "clear" in condition or "sunny" in condition:
            return "clear"
        elif "cloudy" in condition or "overcast" in condition:
            return "overcast"
        elif "rain" in condition or "drizzle" in condition or "storm" in condition:
            return "rain"
        elif "fog" in condition or "mist" in condition or "haze" in condition:
            return "fog"
        else:
            return "other"
    condition = weather_condition_score(data['condition'])
    print(f"Determined weather condition: {condition}")
    if condition == "overcast":
        current_score += 15
    elif condition == "partly cloudy":
        current_score += 10
    elif condition == "clear":
        current_score += 5
    elif condition == "rain":
        current_score += 15
    else:
        current_score += 0
    print(f"Score after weather condition: {current_score}")

    # Wind speed scoring (ideal: windy)
    if 10 <= data['maxwind_mph']:
        current_score += 15
    elif 0 <= data['maxwind_mph'] < 3:
        current_score += 10
    else:
        current_score += 0
    print(f"Score after wind speed: {current_score}")
    # Barometric pressure trend scoring
    if data['pressure_trend_output'] == "falling":
        current_score += 20
    elif data['pressure_trend_output'] == "steady":
        current_score += 10
    else:  # rising
        current_score += 0

    # Moon phase scoring
    if data['moon_phase'] in ["new", "full"]:
        current_score += 15
    else:
        current_score += 0
    print(f"Score after moon phase: {current_score}"   )
    # Time of day scoring
    def time_diff_in_minutes(time1, time2):
        fmt = '%H:%M'
        t1 = datetime.strptime(time1, fmt)
        t2 = datetime.strptime(time2, fmt)
        diff = abs((t2 - t1).total_seconds()) / 60
        return diff
    
    sunset_diff_minutes = time_diff_in_minutes(data['current_time_24hr'], data['sunset_time_24hr'])
    print(f"Sunset diff minutes: {sunset_diff_minutes}")
    sunrise_diff_minutes = time_diff_in_minutes(data['current_time_24hr'], data['sunrise_time_24hr'])
    print(f"Sunrise diff minutes: {sunrise_diff_minutes}")
    
    if abs(sunset_diff_minutes) <=60 or abs(sunrise_diff_minutes) <=60:  # dawn or dusk hours
        current_score += 15
        dawn_dusk_bonus = 0
    elif abs(sunrise_diff_minutes) <=3*60: # morning hours
        current_score += 10
        morning_evening_bonus = 0
    elif abs(sunset_diff_minutes) <=3*60: # evening hours
        current_score += 10
        morning_evening_bonus = 0
    else:
        current_score += 0
        dawn_dusk_bonus = 15
        morning_evening_bonus = 10
    print(f"Current Hour: {data['current_time_24hr']}, Sunset: {data['sunset_time_24hr']}, Sunrise: {data['sunrise_time_24hr']}") 
    print(f"Score after time of day: {current_score}")  
    # Seasonal adjustment
    if season in ["spring", "fall"]:
        current_score += 10
    elif season == "summer":
        current_score += 5 # Summer is less ideal
    else:
        current_score += 0

    # Clamp score to 0–100
    current_score = min(current_score, 100)

    # Rating based on score
    def rating_from_score(score):
        if score >= 80:
            rating = "Excellent"
        elif score >= 60:
            rating = "Good"
        elif score >= 40:
            rating = "Fair"
        else:
            rating = "Poor"
        return rating
    
    current_rating = rating_from_score(current_score)
    dawn_dusk_rating = rating_from_score(current_score + dawn_dusk_bonus)  # Boost rating by 10 points for dawn/dusk
    morning_evening_rating = rating_from_score(current_score + morning_evening_bonus)  # Boost rating by 5 points for morning/evening
    return current_score, current_rating, dawn_dusk_rating, morning_evening_rating
 





