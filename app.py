from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "5965936def06bc0416b2022672873edc"

CITY_COORDS = {
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Ernakulam": {"lat": 9.9816, "lon": 76.2999},
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
}


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form["city"]

        if city in CITY_COORDS:
            lat = CITY_COORDS[city]["lat"]
            lon = CITY_COORDS[city]["lon"]

            url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            )

            try:
                response = requests.get(url, timeout=10)
                data = response.json()

                if response.status_code == 200:

                    temp = data["main"]["temp"]

                    if temp >= 35:
                        prediction = "Very Hot 🔥"
                    elif temp >= 28:
                        prediction = "Warm ☀️"
                    elif temp >= 20:
                        prediction = "Pleasant 🌤️"
                    else:
                        prediction = "Cool ❄️"

                    weather = {
                        "city": city,
                        "temp": temp,
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "description": data["weather"][0]["description"].title(),
                        "prediction": prediction,
                    }
                else:
                    error = data.get("message", "Unable to fetch weather.")

            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        cities=CITY_COORDS.keys(),
        weather=weather,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)