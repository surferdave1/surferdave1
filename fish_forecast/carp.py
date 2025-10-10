# the following code was created with co-pilot, and customized by me

def forecast_carp(data):
    """
    Generate a carp fishing forecast score and rating based on environmental and astronomical inputs.
    """

    # Initialize score
    score = 50

    # Temperature influence
    if 60 <= data['avgtemp_f'] <= 75:
        score += 10
    elif data['avgtemp_f'] < 50 or data['avgtemp_f'] > 85:
        score -= 10

    # Wind influence
    if 2 <= data['wind_mph'] <= 10:
        score += 5
    elif data['wind_mph'] > 15:
        score -= 5

    # Pressure trend
    if data['pressure_trend_output'] == 'rising':
        score += 10
    elif data['pressure_trend_output'] == 'falling':
        score -= 10

    # Humidity
    if 50 <= data['humidity'] <= 80:
        score += 5

    # Moon phase
    moon_bonus = {
        'Full Moon': 10,
        'New Moon': 8,
        'Waxing Crescent': 5,
        'Waning Crescent': 5,
        'First Quarter': 6,
        'Last Quarter': 6
    }
    score += moon_bonus.get(data['moon_phase'], 0)

    # Time of day
    if data['current_hour_24hr'] in range(5, 9) or data['current_hour_24hr'] in range(17, 21):
        score += 10  # Dawn and dusk are prime times
        time_of_day_bonus = 0
    else:
        score += 0
        time_of_day_bonus = 10  # Less optimal times

    # Pressure stability
    pressure_range = data['max_pressure_in_output'] - data['min_pressure_in_output']
    if pressure_range < 0.2:
        score += 5  # Stable pressure is good


    # Morning vs Afternoon pressure
    if data['avg_morning_pressure_in'] > data['avg_afternoon_pressure_in']:
        score += 3  # Morning pressure drop can trigger feeding

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