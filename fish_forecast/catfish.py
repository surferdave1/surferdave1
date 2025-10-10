# the following code was created with co-pilot, and customized by me
def forecast_catfish(data):
    # Assign weights to each variable (customize as needed)
    weights = {
        'temp': 0.15,
        'wind': 0.10,
        'pressure': 0.15,
        'humidity': 0.10,
        'moon': 0.15,
        'sunrise_sunset': 0.10,
        'pressure_trend': 0.10,
        'region': 0.05,
        'condition': 0.10
    }

    # Score temperature (best for catfish: 70-85°F)
    temp_score = max(0, min(1, (85 - abs(data['avgtemp_f'] - 77)) / 15))

    # Score wind (catfish prefer mild wind: 2-10 mph)
    wind_score = max(0, min(1, (10 - abs(data['wind_mph'] - 6)) / 8))

    # Score pressure (stable or slowly falling is best)
    pressure_score = 1 if data['pressure_trend_output'] in ['steady', 'falling slowly'] else 0.5

    # Score humidity (higher is generally better)
    humidity_score = data['humidity'] / 100

    # Score moon phase (full/new moon often better)
    moon_score = 1 if data['moon_phase'].lower() in ['full moon', 'new moon'] else 0.5

    # Score sunrise/sunset (fishing best at dawn/dusk)
    hour = int(data['current_hour_24hr'])
    sunrise_hour = int(data['sunrise_time_24hr'].split(':')[0])
    sunset_hour = int(data['sunset_time_24hr'].split(':')[0])
    if abs(hour - sunrise_hour) <= 2 or abs(hour - sunset_hour) <= 2:
        sunrise_sunset_score = 1
        sunrise_sunset_bonus = 0
    else:
        sunrise_sunset_score = 0.5
        sunrise_sunset_bonus = 0.5

    # Score pressure range (stable range is better)
    pressure_range = data['max_pressure_in_output'] - data['min_pressure_in_output']
    pressure_range_score = 1 if pressure_range < 0.2 else 0.5

    # Score region (customize for your area)
    region_score = 1 if data['region'].lower() in ['midwest', 'south'] else 0.5

    # Score condition (cloudy/rainy often better for catfish)
    condition_score = 1 if data['condition'].lower() in ['cloudy', 'rain', 'overcast'] else 0.5

    # Weighted sum
    score = (
        temp_score * weights['temp'] +
        wind_score * weights['wind'] +
        pressure_score * weights['pressure'] +
        humidity_score * weights['humidity'] +
        moon_score * weights['moon'] +
        sunrise_sunset_score * weights['sunrise_sunset'] +
        pressure_range_score * weights['pressure_trend'] +
        region_score * weights['region'] +
        condition_score * weights['condition']
    ) * 100

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
    
    current_rating = rating_from_score(current_score)
    dawn_dusk_rating = rating_from_score(current_score + sunrise_sunset_bonus)
    morning_evening_rating = rating_from_score(current_score + sunrise_sunset_bonus)

    print(f"Final Score: {current_score}, Current Rating: {current_rating}, Dawn/Dusk Rating: {dawn_dusk_rating}, Morning/Evening Rating: {morning_evening_rating}")
    return current_score, current_rating, dawn_dusk_rating, morning_evening_rating