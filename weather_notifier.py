import time
from sms_sender import send_sms  # Assuming SMS sending function exists
from db_manager import users_collection
import requests  # For fetching weather data from an API

# Replace with your actual weather API key and endpoint
WEATHER_API_KEY = 'your_weather_api_key'
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Mock function to simulate fetching weather alerts for the given location
def get_weather_alert(location):
    """Fetch the weather alert for the given location."""
    try:
        # Assuming location is a city name, or you can modify to take lat/lon
        response = requests.get(WEATHER_API_URL, params={
            'q': location,
            'appid': WEATHER_API_KEY,
            'units': 'metric'  # Optional, to get temperature in Celsius
        })
        if response.status_code == 200:
            data = response.json()
            weather_description = data['weather'][0]['description']
            if "storm" in weather_description or "rain" in weather_description:
                # For simplicity, any storm or rain is considered an alert
                alert = f"Weather Alert for {location}: {weather_description}. Stay safe!"
                return alert
        else:
            print("Error fetching weather data.")
            return None
    except Exception as e:
        print(f"Error fetching weather alert: {e}")
        return None

def start_monitoring(phone):
    """Start disaster monitoring for a specific user."""
    user = users_collection.find_one({"phone": phone, "is_active": True})
    if not user:
        print("Error: User not activated.")
        return

    location = user['location']
    print(f"Monitoring started for {phone} in {location}.")

    while True:
        alert = get_weather_alert(location)
        if alert:
            send_sms(phone, alert)
            print(f"Alert sent to {phone}: {alert}")
        time.sleep(60)  # Check every minute