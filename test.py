import requests

#Function to fetch data
def fetch_mumbai():
    url = "https://api.open-meteo.com/v1/forecast?latitude=19.076&longitude=72.877&current=relative_humidity_2m,precipitation"

    response = requests.get(url)
    return response.json()
#Function for checking risk
def check_weather(rain,humidity):
    if rain > 30 and humidity > 65:
        print("WARNING: High risk of a flash flood or a Cloudburst!")
    else:
        print("Weather seems to be clear!")

weather=fetch_mumbai()
rain = weather["current"]["precipitation"]
humidity = weather["current"]["relative_humidity_2m"]

print(f"Current rain in Mumbai is: {rain}mm")
print(f"Current humidity in Mumbai is:{humidity}%")