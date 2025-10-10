# the following code was created with co-pilot, and customized by me
def forecast_panfish(data):
    """
    Calculate a fishing score and rating for panfish based on environmental conditions.
    
    Parameters:
        data (dict): Dictionary containing all input variables.
    
    Returns:
        dict: Contains 'score' (0–100) and 'rating' (Poor, Fair, Good, Excellent)
    """

    score = 0

    # Temperature (ideal range: 65–75°F)
    if 65 <= data['avgtemp_f'] <= 75:
        score += 20
    elif 60 <= data['avgtemp_f'] <= 80:
        score += 10

    # Wind (ideal: <10 mph)
    if data['wind_mph'] < 10:
        score += 10
    elif data['wind_mph'] < 15:
        score += 5

    # Pressure trend (rising is good)
    if data['pressure_trend_output'] == 'rising':
        score += 10
    elif data['pressure_trend_output'] == 'steady':
        score += 5

    # Humidity (moderate is better)
    if 40 <= data['humidity'] <= 70:
        score += 5

    # Moon phase (full or new moon = better)
    good_moon_phases = ['Full Moon', 'New Moon']
    if data['moon_phase'] in good_moon_phases:
        score += 15
    elif 'First Quarter' in data['moon_phase'] or 'Last Quarter' in data['moon_phase']:
        score += 5

    # Time of day (early morning or evening near sunrise/sunset)
    current_hour = int(data['current_hour_24hr'])
    sunrise_hour = int(data['sunrise_time_24hr'].split(':')[0])
    sunset_hour = int(data['sunset_time_24hr'].split(':')[0])

    if abs(current_hour - sunrise_hour) <= 1 or abs(current_hour - sunset_hour) <= 1:
        score += 15
        time_of_day_bonus = 0
    else:
        score += 0
        time_of_day_bonus = 15

    # Pressure stability (less fluctuation is better)
    pressure_range = data['max_pressure_in_output'] - data['min_pressure_in_output']
    if pressure_range < 0.1:
        score += 10
    elif pressure_range < 0.2:
        score += 5

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