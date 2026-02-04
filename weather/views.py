from django.shortcuts import render


def weather_view(request):
    """Простая страница для тестирования"""
    context = {
        'city': 'Irkutsk',
        'temperature': 20,
        'description': 'Солнечно',
        'humidity': 70,
    }
    return render(request, 'weather/weather.html', context)

def about_view(request):
    return render(request, 'weather/about.html')