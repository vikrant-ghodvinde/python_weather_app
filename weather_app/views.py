import requests
from django.shortcuts import render
from .models import Weather

def get_weather_data(city):
    api_key = 'c85a1871ba6deab988c83c2ee5a8e84f'
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

    response = requests.get(base_url, params=params)
    data = response.json()

    if data['cod'] == 200:
        weather = {
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
        }
        Weather.objects.create(**weather)

def weather(request):
    city = 'New York'  # Default city
    if request.method == 'POST':
        city = request.POST['city']
        get_weather_data(city)

    weather_data = Weather.objects.filter(city=city).order_by('-timestamp').first()
    return render(request, 'weather.html', {'weather_data': weather_data})
