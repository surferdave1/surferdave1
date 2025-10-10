from datetime import datetime

# the following code was created with co-pilot, and customized by me
def forecast_salmon(data):
    score = 0

    # Temperature scoring
    if 50 <= data['avgtemp_f'] <= 60:
        score += 15
    elif 45 <= data['avgtemp_f'] <= 65:
        score += 10
    else:
        score += 5

    # Wind scoring
    if data['wind_mph'] <= 5:
        score += 10
    elif data['wind_mph'] <= 10:
        score += 5

    # Pressure trend
    if data['pressure_trend_output'] == 'rising':
        score += 10
    elif data['pressure_trend_output'] == 'steady':
        score += 5

    # Humidity
    if 40 <= data['humidity'] <= 70:
        score += 10

    # Moon phase
    good_moon_phases = ['Full Moon', 'New Moon']
    if data['moon_phase'] in good_moon_phases:
        score += 10
    else:
        score += 5

    # Time of day
    if 5 <= data['current_hour_24hr'] <= 8 or 17 <= data['current_hour_24hr'] <= 20:
        score += 15
    else:
        score += 5
        # Time of day (early morning or evening near sunrise/sunset)
    current_hour = int(data['current_hour_24hr'])
    sunrise_hour = int(data['sunrise_time_24hr'].split(':')[0])
    sunset_hour = int(data['sunset_time_24hr'].split(':')[0])

    if abs(current_hour - sunrise_hour) <= 1 or abs(current_hour - sunset_hour) <= 1:
        score += 10
        time_of_day_bonus = 0
    else:
        score += 0
        time_of_day_bonus = 10

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
    dawn_dusk_rating = rating_from_score(current_score + time_of_day_bonus)  # Boost rating by 10 points for dawn/dusk
    morning_evening_rating = rating_from_score(current_score + time_of_day_bonus)  # Boost rating by 5 points for morning/evening
    return current_score, current_rating, dawn_dusk_rating, morning_evening_rating
