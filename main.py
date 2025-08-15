import time
import traceback
import schedule
import config
from weather import get_location_by_ip, fetch_current_weather, categorize_weather
from notifier import alert_user

def build_message_from_categories(categories, temp, location_info):
    cats = set(categories)
    if "rainy" in cats and ("hot" in cats or temp is not None and temp >= config.HOT_THRESHOLD):
        return "Bring your umbrella and wear closed toe shoes!"
    if "sunny" in cats:
        return "Bring your sunglasses and a water bottle!"
    if "snow" in cats:
        return "Wear warm boots and a coat, it's going to snow!"
    if "storm" in cats:
        return "Severe weather, be cautious while driving and bring an umbrella!"
    if "rainy" in cats:
        return "Bring an umbrella!"
    if "cloudy" in cats:
        return "It's cloudy, you might not need sunglasses!"
    if "hot" in cats:
        return "It's hot today, bring water and wear lightweight clothes!"
    if "cold" in cats:
        return "It's cold, bring a jacket!"
    if "mild" in cats:
        return "Mild weather, a light jacket would do nicely!"
    return "Weather looks normal, have a great day!"

def do_weather_check_and_alert():
    try:
        loc = get_location_by_ip()
        lat = loc.get("lat")
        lon = loc.get("lon")
        city = loc.get("city", "your area")

        w = fetch_current_weather(lat, lon)
        categorized = categorize_weather(w)
        categories = categorized["categories"]
        temp = categorized["temp"]

        message = build_message_from_categories(categories, temp, loc)
        title = f"Morning weather — {city}"
        body_lines = [
            f"{title}",
            f"Conditions: {categorized['main']} — {categorized['description']}",
            f"Temperature: {temp} {('°F' if config.UNITS=='imperial' else '°C')}",
            f"Categories: {', '.join(categories)}",
            "",
            f"ALERT: {message}",
        ]
        alert_user(title, message, email_body="\n".join(body_lines))

    except Exception as e:
        print("Error during weather check:", e)
        traceback.print_exc()

def schedule_daily_8am():
    schedule.every().day.at("08:00").do(do_weather_check_and_alert)
    print("Scheduled daily weather alert at 08:00 local time.")

def main():
    print("Starting morning weather email alert program.")
    if config.RUN_IMMEDIATE_TEST_CHECK:
        do_weather_check_and_alert()
    schedule_daily_8am()
    try:
        while True:
            schedule.run_pending()
            time.sleep(20)
    except KeyboardInterrupt:
        print("Shutting down.")

if __name__ == "__main__":
    main()
