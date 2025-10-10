# the following code was created with co-pilot, and customized by me
def forecast_crappie(data):
    # Example weights (tune as needed)
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

    # Temperature: best between 55-70°F
    temp_score = max(0, min(1, (70 - abs(data['avgtemp_f'] - 62)) / 15))

    # Wind: best below 10 mph
    wind_score = max(0, min(1, (10 - data['wind_mph']) / 10))

    # Pressure: stable or slowly rising is best
    pressure_score = 1 if data['pressure_trend_output'] in ['steady', 'rising'] else 0.5

    # Humidity: moderate is best (40-70%)
    humidity_score = max(0, min(1, (70 - abs(data['humidity'] - 55)) / 30))

    # Moon phase: full/new moon is best
    moon_phase = data['moon_phase'].lower()
    if moon_phase in ['full', 'new']:
        moon_score = 1
    elif moon_phase in ['waxing gibbous', 'waning crescent']:
        moon_score = 0.7
    else:
        moon_score = 0.5

    # Sunrise/Sunset: fishing best at dawn/dusk
    hour = int(data['current_hour_24hr'])
    sunrise_hour = int(data['sunrise_time_24hr'].split(':')[0])
    sunset_hour = int(data['sunset_time_24hr'].split(':')[0])
    if abs(hour - sunrise_hour) <= 2 or abs(hour - sunset_hour) <= 2:
        sunrise_sunset_score = 1
        sunrise_sunset_bonus = 0
    else:
        sunrise_sunset_score = 0.5
        sunrise_sunset_bonus = 0.5

    # Region: adjust for local knowledge
    region_score = 1 if data['region'].lower() in ['midwest', 'south'] else 0.7

    # Condition: clear/cloudy/rain
    condition = data['condition'].lower()
    if condition in ['overcast', 'partly cloudy']:
        condition_score = 1
    elif condition == 'clear':
        condition_score = 0.7
    else:
        condition_score = 0.5

    # Combine scores
    score = (
        temp_score * weights['temp'] +
        wind_score * weights['wind'] +
        pressure_score * weights['pressure'] +
        humidity_score * weights['humidity'] +
        moon_score * weights['moon'] +
        sunrise_sunset_score * weights['sunrise_sunset'] +
        region_score * weights['region'] +
        condition_score * weights['condition'] +
        pressure_score * weights['pressure_trend']
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
