from flask import Flask, render_template, request
import requests


app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def home():
    city = "kampala"
    data = weather_info(city)
    clouds, temp, humidity, pressure, wind = (
        data["clouds"],
        data["temp"],
        data["humidity"],
        data["pressure"],
        data["wind"],
    )
    return render_template(
        "index.htm",
        temp=temp,
        city=city.upper(),
        HUMUDITY=humidity,
        CLOUDS=clouds,
        wind_speed=wind,
        PRESSURE=pressure,
    )


@app.route("/weather", methods=["POST", "GET"])
def weather_info():
    city = request.form.get("city", "")
    if city != "":
        data = weather_info(city)
        clouds, temp, humidity, pressure, wind = (
            data["clouds"],
            data["temp"],
            data["humidity"],
            data["pressure"],
            data["wind"],
        )

        return render_template(
            "index.htm",
            temp=temp,
            city=city.upper(),
            HUMUDITY=humidity,
            CLOUDS=clouds,
            wind_speed=wind,
            PRESSURE=pressure,
        )
    else:
        city = "Kampala"
        data = weather_info(city)
        render_template(
            "index.htm",
            temp=data["temp"],
            city=city.upper(),
            HUMUDITY=data["humidity"],
            CLOUDS=data["clouds"],
            wind_speed=data["wind"],
            PRESSURE=data["pressure"],
        )


def weather_info(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "0453b2e122a1c2c07a4905e2c43f6e7a"
    params = {"appid": api_key, "q": city, "units": "metric"}
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    data = response.json()
    clouds = data["clouds"]["all"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    data = {
        "temp": temp,
        "clouds": clouds,
        "humidity": humidity,
        "pressure": pressure,
        "wind": wind,
    }
    return data


if __name__ == "__main__":
    app.run(debug=True)
