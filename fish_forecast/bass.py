def forecast_bass(date, avgtemp_f, condition, maxwind_mph,moon_phase, current_time, season, sunset_time_24hr, sunrise_time):
    score = 0
    print(f"score: {score}")

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
    season = season_from_date(date)
    print(f"Determined season: {season}")
    # Temperature scoring (ideal range: 55–75°F)
    if season=="spring" and 50 <= avgtemp_f <= 70:
        score += 10
    elif season=="summer" and 70 <= avgtemp_f <= 85:
        score += 10
    elif season=="fall" and 50 <= avgtemp_f <= 65:
        score += 10   
    elif season=="winter" and 35 <= avgtemp_f <= 50:
        score += 10   
    else:
        score += 0
    print(f"Avg Temp: {avgtemp_f}, Season: {season}"   )
    print(f"Score after temperature: {score}"   )
    
    # Weather scoring
    def weather_condition_score(condition):
        condition = condition.lower()
        if "clear" in condition or "sunny" in condition:
            return "clear"
        elif "cloud" in condition or "overcast" in condition:
            return "overcast"
        elif "rain" in condition or "drizzle" in condition or "storm" in condition:
            return "rain"
        elif "fog" in condition or "mist" in condition or "haze" in condition:
            return "fog"
        else:
            return "other"
    condition = weather_condition_score(condition)
    print(f"Determined weather condition: {condition}")
    if condition == "overcast":
        score += 15
    elif condition == "partly cloudy":
        score += 10
    else:
        score += 0
    print(f"Score after weather condition: {score}")

    # Wind speed scoring (ideal: windy)
    if 10 <= maxwind_mph:
        score += 15
    elif 0 <= maxwind_mph < 3:
        score += 10
    else:
        score += 0

    # Barometric pressure trend scoring
    #if pressure_trend == "falling":
        #score += 20
    #elif pressure_trend == "steady":
       # score += 10
    #else:  # rising
       # score += 0

    # Moon phase scoring
    if moon_phase in ["new", "full"]:
        score += 15
    else:
        score += 0
    print(f"Score after moon phase: {score}"   )
    # Time of day scoring
    if abs(current_time - sunset_time_24hr) <=1:  # dawn or dusk hours
        score += 15
    elif abs(current_time - sunrise_time) <=3: # morning hours
        score += 10
    elif abs(current_time - sunset_time_24hr) <=3: # evening hours
        score += 10
    else:
        score += 0
    print(f"Current Hour: {current_time}, Sunset Hour: {sunset_time_24hr}, Sunrise Hour: {sunrise_time}") 
    print(f"Score after time of day: {score}")  
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




score, rating = forecast_bass()

print(f"Fishing Quality Score: {score}/100")
print(f"Rating: {rating}")