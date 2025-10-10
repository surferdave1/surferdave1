from datetime import datetime

# the following code was created with co-pilot, and customized by me
def forecast_muskie(data):
    score = 0

    # Moon phase scoring
    moon_phase_scores = {
        "New Moon": 20,
        "Full Moon": 20,
        "First Quarter": 10,
        "Last Quarter": 10,
        "Waxing Crescent": 5,
        "Waning Crescent": 5,
        "Waxing Gibbous": 15,
        "Waning Gibbous": 15
    }
    score += moon_phase_scores.get(data["moon_phase"], 0)

    # Pressure trend
    if data["pressure_trend_output"] == "rising":
        score += 15
    elif data["pressure_trend_output"] == "falling":
        score += 5
    else:
        score += 10

    # Wind
    if 5 <= data["wind_mph"] <= 15:
        score += 10
    elif data["wind_mph"] > 15:
        score += 5

    # Temperature
    if 60 <= data["avgtemp_f"] <= 75:
        score += 15
    elif 50 <= data["avgtemp_f"] < 60 or 75 < data["avgtemp_f"] <= 80:
        score += 10

    # Time of day
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
    
    if abs(sunset_diff_minutes) <=120 or abs(sunrise_diff_minutes) <=120:  # dawn or dusk hours
        score += 15
        dawn_dusk_bonus = 0
    else:
        score += 0
        dawn_dusk_bonus = 15
        
    # Humidity
    if 40 <= data["humidity"] <= 70:
        score += 10

       # Clamp score to 0–100
    current_score = min(score, 100)

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
    morning_evening_rating = rating_from_score(current_score + dawn_dusk_bonus)  # Boost rating by 5 points for morning/evening
    return current_score, current_rating, dawn_dusk_rating, morning_evening_rating
 
