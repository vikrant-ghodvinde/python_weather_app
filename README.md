# python_weather_app
Creating a weather app in Python using Django involves several steps, including setting up a Django project, integrating a weather API, creating views, and designing templates. In this example, I'll show you how to create a simple weather app using the OpenWeatherMap API. You can adapt this to use any other weather API you prefer.

Note: You'll need to sign up for an API key from OpenWeatherMap (or your chosen weather API provider) and replace 'YOUR_API_KEY' with your actual API key.

Let's get started:

1. Setup Django Project:

If you haven't already, install Django by running:

pip install Django


Create a new Django project and app:

django-admin startproject weather_project
cd weather_project
python manage.py startapp weather_app


2. Configure your project:
In your weather_project/settings.py, add 'weather_app' to the INSTALLED_APPS list.


3. Create Models:
In weather_app/models.py, create a model to store weather information (you can extend it as needed):

from django.db import models

class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city


Run migrations to create the database table:

python manage.py makemigrations
python manage.py migrate


4. Create Views:
In weather_app/views.py, create a view that fetches weather data from the OpenWeatherMap API:

import requests
from django.shortcuts import render
from .models import Weather

def get_weather_data(city):
    api_key = 'YOUR_API_KEY'
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
    return render(request, 'weather_app/weather.html', {'weather_data': weather_data})


5. Create Templates:
Create a folder named templates in your weather_app directory. Inside that folder, create a file named weather.html to display weather information:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Weather App</title>
</head>
<body>
    <h1>Weather App</h1>
    <form method="post">
        {% csrf_token %}
        <label for="city">Enter a city: </label>
        <input type="text" name="city" id="city">
        <input type="submit" value="Get Weather">
    </form>
    {% if weather_data %}
        <h2>Weather in {{ weather_data.city }}</h2>
        <p>Temperature: {{ weather_data.temperature }}°C</p>
        <p>Description: {{ weather_data.description }}</p>
        <img src="http://openweathermap.org/img/w/{{ weather_data.icon }}.png" alt="Weather Icon">
    {% endif %}
</body>
</html>


6. Configure URLs:
In weather_project/urls.py, define the URL patterns:

from django.contrib import admin
from django.urls import path
from weather_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', views.weather, name='weather'),
]

Then, include these URLs in your project's urls.py.


7. Run the Development Server:
Start the development server by running:

python manage.py runserver

Visit http://127.0.0.1:8000/weather/ in your browser to use the weather app.

This is a basic example of a weather app using Django and the OpenWeatherMap API. You can further enhance the app by adding error handling, user authentication, and more features based on your requirements.


<!-- WEATHER API LINK -->
<!-- get your api from here -->
https://home.openweathermap.org/