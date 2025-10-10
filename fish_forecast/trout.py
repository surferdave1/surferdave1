from datetime import datetime

# the following code was created with co-pilot, and customized by me
def forecast_trout(data):
    # Assign weights to different factors based on their importance to trout fishing
    weights = {
        'avgtemp_f': 0.1,
        'maxwind_mph': -0.1,
        'pressure_in': 0.2,
        'wind_mph': -0.1,
        'humidity': 0.1,
        'moon_phase': 0.15,
        'pressure_trend_output': 0.1,
        'avg_morning_pressure_in': 0.1,
        'avg_afternoon_pressure_in': 0.1
    }

    # Normalize and score each factor
    score = 0

    # Temperature: Ideal range for trout is 50–60°F
    temp_score = max(0, 1 - abs(data['avgtemp_f'] - 55) / 20)
    score += temp_score * weights['avgtemp_f'] * 100

    # Wind: Less wind is better
    wind_score = max(0, 1 - data['maxwind_mph'] / 30)
    score += wind_score * abs(weights['maxwind_mph']) * 100

    # Pressure: Stable or rising pressure is good
    pressure_score = max(0, min(data['pressure_in'] / 30, 1))
    score += pressure_score * weights['pressure_in'] * 100

    # Wind speed
    wind_mph_score = max(0, 1 - data['wind_mph'] / 30)
    score += wind_mph_score * abs(weights['wind_mph']) * 100

    # Humidity: Moderate humidity is preferred
    humidity_score = max(0, 1 - abs(data['humidity'] - 50) / 50)
    score += humidity_score * weights['humidity'] * 100

    # Moon phase: Full and new moons are better
    moon_phase_score = 1 if data['moon_phase'].lower() in ['full moon', 'new moon'] else 0.5
    score += moon_phase_score * weights['moon_phase'] * 100

    # Pressure trend: Rising is good
    pressure_trend_score = 1 if data['pressure_trend_output'].lower() == 'rising' else 0.5
    score += pressure_trend_score * weights['pressure_trend_output'] * 100

    # Morning pressure
    morning_pressure_score = max(0, min(data['avg_morning_pressure_in'] / 30, 1))
    score += morning_pressure_score * weights['avg_morning_pressure_in'] * 100

    # Afternoon pressure
    afternoon_pressure_score = max(0, min(data['avg_afternoon_pressure_in'] / 30, 1))
    score += afternoon_pressure_score * weights['avg_afternoon_pressure_in'] * 100
    
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
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        else:
            return "Poor"

    # Apply bonus (if applicable — you may want to define `time_of_day_bonus` elsewhere)
    time_of_day_bonus = 0  # Placeholder if not defined elsewhere

    current_rating = rating_from_score(current_score)
    dawn_dusk_rating = rating_from_score(current_score + time_of_day_bonus)
    morning_evening_rating = rating_from_score(current_score + time_of_day_bonus)

    return current_score, current_rating, dawn_dusk_rating, morning_evening_rating