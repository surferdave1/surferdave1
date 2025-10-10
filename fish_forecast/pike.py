import datetime

# the following code was created with co-pilot, and customized by me
def forecast_pike(data):
    score = 0

    # Temperature scoring (optimal range for pike activity: 50–70°F)
    if 50 <= data['avgtemp_f'] <= 70:
        score += 20
    elif 45 <= data['avgtemp_f'] < 50 or 70 < data['avgtemp_f'] <= 75:
        score += 10

    # Wind scoring (moderate wind is good: 5–15 mph)
    if 5 <= data['wind_mph'] <= 15:
        score += 15
    elif 2 <= data['wind_mph'] < 5 or 15 < data['wind_mph'] <= 20:
        score += 5

    # Pressure scoring (stable or rising pressure is favorable)
    pressure_trend = data['pressure_trend_output'].lower()
    if pressure_trend == "rising":
        score += 15
    elif pressure_trend == "stable":
        score += 10
    elif pressure_trend == "falling":
        score += 5

    # Humidity scoring (moderate humidity is better)
    if 40 <= data['humidity'] <= 70:
        score += 10
    elif 30 <= data['humidity'] < 40 or 70 < data['humidity'] <= 80:
        score += 5

    # Moon phase scoring (new moon and full moon are favorable)
    favorable_moon_phases = ["New Moon", "Full Moon"]
    if data['moon_phase'] in favorable_moon_phases:
        score += 10
    else:
        score += 5

    # Time of day scoring (early morning and late evening are best)
    try:
        current_time = datetime.datetime.strptime(data['current_time_24hr'], "%H:%M")
        sunrise_time = datetime.datetime.strptime(data['sunrise_time_24hr'], "%H:%M")
        sunset_time = datetime.datetime.strptime(data['sunset_time_24hr'], "%H:%M")

        if current_time <= sunrise_time + datetime.timedelta(hours=2) or current_time >= sunset_time - datetime.timedelta(hours=2):
            score += 15
            time_of_day_bonus = 0
        else:
            score += 5
            time_of_day_bonus = 10
    except Exception:
        score += 5  # fallback score if time parsing fails
        time_of_day_bonus = 0

    # Pressure variation scoring
    pressure_variation = data['max_pressure_in_output'] - data['min_pressure_in_output']
    if pressure_variation < 0.2:
        score += 10
    elif pressure_variation < 0.5:
        score += 5

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
    dawn_dusk_rating = rating_from_score(current_score + time_of_day_bonus)
    morning_evening_rating = rating_from_score(current_score + time_of_day_bonus)

    return current_score, current_rating, dawn_dusk_rating, morning_evening_rating