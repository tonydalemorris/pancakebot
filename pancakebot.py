import logging
from logging.handlers import RotatingFileHandler
import groupy
from flask import Flask, request
import forecastio
from geopy.geocoders import Nominatim

application = Flask(__name__)
application.config.from_object('settings')


# clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy, partly-cloudy-day, or partly-cloudy-night
WEATHER_ICONS = {
  'clear-day': '☀',
  'clear-night': '🌑',
  'rain': '☔',
  'snow': '☃❄',
  'sleet': '☃❄',
  'wind': '🌬',
  'fog': '≈',
  'cloudy': '☁',
  'partly-cloudy-day': '⛅',
  'partly-cloudy-night': '☁🌑'
}

def display_weather(bot, message):
  api_key = application.config['FORECASTIO_API_KEY']

  if api_key is None:
    print('FORECASTIO_API_KEY not configured, not displaying weather information!')

  geolocator = Nominatim()
  location = geolocator.geocode(message or 'Austin, TX')
  forecast = forecastio.load_forecast(api_key, location.latitude, location.longitude)
  current = forecast.currently()
  icon = WEATHER_ICONS[current.icon] or ''

  bot.post('{0}  {1} {2}° (feels like {3}°)'.format(icon, current.summary, round(current.temperature), round(current.apparentTemperature)))

@application.route('/pancakebot', methods=['POST'])
def hello():
  data = request.get_json()
  bot = groupy.Bot.list().first

  user = data['name']
  message = data['text'].lower()

  try:
    if message.startswith('!weather'):
      display_weather(bot, message[len('!weather'):].strip())
  except Exception as e:
    print(e)

  return 'OK'

if __name__ == '__main__':
  application.run(host='0.0.0.0', port=5555)
