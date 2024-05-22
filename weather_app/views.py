from django.shortcuts import render
import requests
from datetime import datetime
import pytz

def index(request):
    weather = None
    units = 'metric'

    def format_time(date):
        return date.strftime('%H:%M')

    def format_day(date):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[date.weekday()]

    tz = pytz.timezone('Asia/Karachi')
    current_time = format_time(datetime.now(tz))
    current_day = format_day(datetime.now(tz))

    if request.method == 'POST':
        location = request.POST.get('location')
        units = request.POST.get('units', 'metric')
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&units={units}&appid=93c5e66aad50ba77f255b651041326ed'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'temp_max': data['main']['temp_max'],
                'temp_min': data['main']['temp_min'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed'],
                'units': units,
                'widgetId': 'cdcd5f35988b1'
            }
        else:
            weather = {'error': 'City not found'}

    return render(request, 'index.html', {'weather': weather, 'units': units, 'current_time': current_time, 'current_day': current_day})
