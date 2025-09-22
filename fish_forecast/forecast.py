def bass_fishing_quality(air_temp, weather, wind_speed, pressure_trend, moon_phase, time_of_day, season, ):
    score = 0

    # Temperature scoring (ideal range: 55–75°F)
    if season=="spring" and 50 <= air_temp <= 70:
        score += 10
    elif season=="summer" and 70 <= air_temp <= 85:
        score += 10
    elif season=="fall" and 50 <= air_temp <= 65:
        score += 10   
    elif season=="winter" and 35 <= air_temp <= 50:
        score += 10   
    else:
        score += 0

    # Weather scoring
    if weather == "overcast":
        score += 15
    elif weather == "partly cloudy":
        score += 10
    else:
        score += 0

    # Wind speed scoring (ideal: windy)
    if 10 <= wind_speed:
        score += 15
    elif 0 <= wind_speed < 3:
        score += 10
    else:
        score += 0

    # Barometric pressure trend scoring
    if pressure_trend == "falling":
        score += 20
    elif pressure_trend == "steady":
        score += 10
    else:  # rising
        score += 0

    # Moon phase scoring
    if moon_phase in ["new", "full"]:
        score += 15
    else:
        score += 0

    # Time of day scoring
    if time_of_day in ["dawn", "dusk"]:
        score += 15
    elif time_of_day in ["morning", "evening"]:
        score += 10
    else:
        score += 0
    
    # Seasonal adjustment
    if season in ["spring", "fall"]:
        score += 10
    elif season == "summer":
        score += 5 # Summer is less ideal
    else:
        score += 0

    # Clamp score to 0–100
    score = min(score, 100)

    # Rating based on score
    if score >= 80:
        rating = "Excellent"
    elif score >= 60:
        rating = "Good"
    elif score >= 40:
        rating = "Fair"
    else:
        rating = "Poor"

    return score, rating


# Example mock data
mock_data = {
    "air_temp": 68,
    "weather": "overcast",
    "wind_speed": 10,
    "pressure_trend": "falling",
    "moon_phase": "full",
    "time_of_day": "dawn",
    "season": "spring"
}

score, rating = bass_fishing_quality(**mock_data)

print(f"Fishing Quality Score: {score}/100")
print(f"Rating: {rating}")