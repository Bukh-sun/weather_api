from django.shortcuts import render
import requests
import requests_cache
import json


requests_cache.install_cache('weather_cache', expire_after=300, allowable_methods=('GET',))
def weather_view(request):
    city = request.GET.get('city', 'Irkutsk')

    cities = {
        'Moscow': {'lat': 55.7558, 'lon': 37.6173, 'name': 'Москва'},
        'Irkutsk': {'lat': 52.2966, 'lon': 104.2756, 'name': 'Иркутск'},
        'Sochi': {'lat': 43.5855, 'lon': 39.7231, 'name': 'Сочи'},
        'London': {'lat': 51.5074, 'lon': -0.1278, 'name': 'Лондон'},
        'Paris': {'lat': 48.8566, 'lon': 2.3522, 'name': 'Париж'},
    }

    if city not in cities:
        city = 'Irkutsk'

    coords = cities[city]

    try:
        params = {
            'latitude': coords['lat'],
            'longitude': coords['lon'],
            'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code',
            'timezone': 'auto'
        }

        response = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params=params,
            timeout=5
        )


        if response.status_code == 200:
            data = response.json()

            current = data.get('current', {})

            weather_info = get_weather_info(current.get('weather_code', 0))

            context = {
                'city_name': cities[city]['name'],
                'temperature': round(current.get('temperature_2m', 0), 1),
                'humidity': int(current.get('relative_humidity_2m', 0)),
                'wind_speed': round(current.get('wind_speed_10m', 0), 1),
                'description': weather_info['description'],
                'icon': weather_info['icon'],
                'cities': cities,
                'selected_city': city,
                'city_names': set(cities)
            }

            return render(request, 'weather/weather.html', context)
        else:
            return render(request, 'weather/error.html', {
                'error': f'Ошибка API: {response.status_code}'
            })

    except Exception as e:
        return render(request, 'weather/error.html', {
            'error': f'Произошла ошибка: {str(e)}'
        })


def get_weather_info(weather_code):
    weather_codes = {
        0: {'description': 'Ясно', 'icon': '☀️'},
        1: {'description': 'Преимущественно ясно', 'icon': '🌤️'},
        2: {'description': 'Переменная облачность', 'icon': '⛅'},
        3: {'description': 'Пасмурно', 'icon': '☁️'},
        45: {'description': 'Туман', 'icon': '🌫️'},
        48: {'description': 'Изморозь', 'icon': '🌫️'},
        51: {'description': 'Легкая морось', 'icon': '🌦️'},
        53: {'description': 'Умеренная морось', 'icon': '🌧️'},
        55: {'description': 'Сильная морось', 'icon': '🌧️'},
        61: {'description': 'Небольшой дождь', 'icon': '🌦️'},
        63: {'description': 'Умеренный дождь', 'icon': '🌧️'},
        65: {'description': 'Сильный дождь', 'icon': '⛈️'},
        71: {'description': 'Небольшой снег', 'icon': '🌨️'},
        73: {'description': 'Умеренный снег', 'icon': '🌨️'},
        75: {'description': 'Сильный снег', 'icon': '❄️'},
        80: {'description': 'Небольшие ливни', 'icon': '🌦️'},
        81: {'description': 'Умеренные ливни', 'icon': '🌧️'},
        82: {'description': 'Сильные ливни', 'icon': '⛈️'},
        95: {'description': 'Гроза', 'icon': '⛈️'},
    }

    return weather_codes.get(int(weather_code), {'description': 'Неизвестно', 'icon': '❓'})


def about_view(request):
    return render(request, 'weather/about.html')