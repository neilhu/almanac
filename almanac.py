import os
import argparse
from datetime import date
import json
from urllib import request

from astral import Astral


def format_sun_times(city_name: str) -> str:
    """Return HTML for sunrise/sunset and moon phase information."""

    astral = Astral()
    astral.solar_depression = "civil"
    city = astral[city_name]
    sun = city.sun(date=date.today(), local=True)

    def _clean_time(value):
        return str(value).split(" ", 2)[1].replace("-04:00", " ")

    moon_phase = city.moon_phase(date=date.today())
    moon_description = {
        0: "New moon",
        7: "First quarter",
        14: "Full moon",
    }.get(moon_phase, "Last quarter")

    return "".join(
        [
            "<h2>Sun and Moon</h2>",
            f"Dawn:    {_clean_time(sun['dawn'])}<p>",
            f"Sunrise: {_clean_time(sun['sunrise'])}<p>",
            f"Noon:    {_clean_time(sun['noon'])}<p>",
            f"Sunset:  {_clean_time(sun['sunset'])}<p>",
            f"Dusk:    {_clean_time(sun['dusk'])}<p>",
            f"Moon:    {moon_description}",
        ]
    )


def _load_json(url: str) -> dict:
    with request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))


def _get_api_key(api_key: str | None) -> str:
    key = api_key or os.getenv("WUNDERGROUND_API_KEY", "").strip()
    if not key:
        raise ValueError(
            "A Weather Underground API key is required. "
            "Pass it via --api-key or set WUNDERGROUND_API_KEY."
        )
    return key


def format_weather(city: str = "Boston", api_key: str | None = None) -> str:
    """Return HTML for current conditions and almanac data."""

    key = _get_api_key(api_key)

    conditions = _load_json(
        f"http://api.wunderground.com/api/{key}/geolookup/conditions/q/MA/{city}.json"
    )

    almanac = _load_json(
        f"http://api.wunderground.com/api/{key}/geolookup/almanac/q/MA/{city}.json"
    )

    current = conditions["current_observation"]
    almanac_data = almanac["almanac"]

    return "".join(
        [
            "<h2>Current Weather</h2>",
            f"Current weather:     {current['weather']}<p>",
            f"Current temperature: {current['temp_f']} F<p>",
            f"Current relative humidity: {current['relative_humidity']}<p>",
            f"Current wind:        {current['wind_string']}<p>",
            f"Current pressure {current['pressure_in']} {current['pressure_trend']}<p>",
            f"Current dewpoint: {current['dewpoint_f']} F<p>",
            f"Current windchill: {current['windchill_f']} F<p>",
            f"Feels like: {current['feelslike_f']} F<p>",
            f"Record low is:  {almanac_data['temp_low']['record']['F']} F in {almanac_data['temp_low']['recordyear']}<p>",
            f"Record high is: {almanac_data['temp_high']['record']['F']} F in {almanac_data['temp_high']['recordyear']}<p>",
        ]
    )


def build_html(city: str = "Boston", api_key: str | None = None) -> str:
    return "\n".join(
        [
            "<html>",
            "<body>",
            format_sun_times(city),
            "<p>",
            format_weather(city, api_key),
            "</body>",
            "</html>",
        ]
    )


def main(output_file: str = "index.html", city: str = "Boston", api_key: str | None = None) -> None:
    html = build_html(city, api_key)
    with open(output_file, "w", encoding="utf-8") as file_handle:
        file_handle.write(html)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a sun, moon, and weather almanac page.")
    parser.add_argument("--city", default="Boston", help="City to query (default: Boston)")
    parser.add_argument("--output", default="index.html", help="Output HTML file path (default: index.html)")
    parser.add_argument(
        "--api-key",
        dest="api_key",
        default=None,
        help="Weather Underground API key (falls back to WUNDERGROUND_API_KEY env var)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    cli_args = parse_args()
    main(output_file=cli_args.output, city=cli_args.city, api_key=cli_args.api_key)
