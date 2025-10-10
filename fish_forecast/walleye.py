
# the following code was created with co-pilot, and customized by me
def forecast_walleye(data):
    score = 0

    # Temperature sweet spot for walleye (50–70°F)
    if 50 <= data['avgtemp_f'] <= 70:
        score += 20
    elif 45 <= data['avgtemp_f'] <= 75:
        score += 10

    # Wind: moderate wind is good (5–15 mph)
    if 5 <= data['wind_mph'] <= 15:
        score += 15
    elif 2 <= data['wind_mph'] <= 20:
        score += 5

    # Pressure trend: rising pressure is generally good
    if data['pressure_trend_output'] == 'rising':
        score += 15
    elif data['pressure_trend_output'] == 'steady':
        score += 5

    # Moon phase: full and new moon are best
    if data['moon_phase'].lower() in ['full moon', 'new moon']:
        score += 15
    elif data['moon_phase'].lower() in ['waxing crescent', 'waning crescent']:
        score += 5

    # Time of day: early morning or dusk
    hour = int(data['current_hour_24hr'])
    sunrise = int(data['sunrise_time_24hr'].split(':')[0])
    sunset = int(data['sunset_time_24hr'].split(':')[0])
    if sunrise <= hour <= sunrise + 2 or sunset - 2 <= hour <= sunset:
        score += 15
        time_of_day_bonus = 0
    else:
        score += 0
        time_of_day_bonus = 15

    # Humidity: moderate humidity is better
    if 40 <= data['humidity'] <= 70:
        score += 10

    # Pressure stability
    pressure_range = data['max_pressure_in_output'] - data['min_pressure_in_output']
    if pressure_range < 0.2:
        score += 10

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
