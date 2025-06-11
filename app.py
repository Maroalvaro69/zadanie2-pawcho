from flask import Flask, render_template, request
import datetime
import requests

app = Flask(__name__)
author = "Marek Górnicki"
port = 5000

LOCATIONS = {
    "Polska": {"Warszawa": (52.23, 21.01)},
    "Niemcy": {"Berlin": (52.52, 13.41)}
}

@app.route("/", methods=["GET", "POST"])
def index():
    weather_info = None
    if request.method == "POST":
        country = request.form.get("country").strip()
        city = request.form.get("city").strip()
        lat, lon = LOCATIONS[country][city]

        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            weather = data.get("current_weather", {})
            temp = weather.get("temperature")
            windspeed = weather.get("windspeed")
            weather_info = f"Pogoda w {city}, {country}: {temp}°C, wiatr {windspeed} km/h"
        else:
            weather_info = "Nie udało się pobrać danych pogodowych."

    return render_template("index.html", weather=weather_info)

if __name__ == "__main__":
    now = datetime.datetime.now()
    print(f"Aplikacja uruchomiona: {now}")
    print(f"Autor: {author}")
    print(f"Port: {port}")
    app.run(host="0.0.0.0", port=port)
