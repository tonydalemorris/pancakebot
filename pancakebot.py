import logging
from logging.handlers import RotatingFileHandler
import groupy
from flask import Flask, request
import forecastio
from geopy.geocoders import Nominatim
import giphypop

application = Flask(__name__)
application.config.from_object('settings')

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

commands = {}

def command(cmd):
  def wrapped_command(function):
    def wrapper(*args, **kwargs):
      function(*args, **kwargs)
    if cmd not in commands:
      commands[cmd] = []
    commands[cmd].append(wrapper)
  return wrapped_command

@command('!weather')
def weather(bot, message, author=None):
  api_key = application.config['FORECASTIO_API_KEY']

  if api_key is None:
    print('FORECASTIO_API_KEY not configured, not displaying weather information!')

  geolocator = Nominatim()
  location = geolocator.geocode(message or 'Austin, TX')
  forecast = forecastio.load_forecast(api_key, location.latitude, location.longitude)
  current = forecast.currently()
  icon = WEATHER_ICONS[current.icon] or ''

  post = '{0}  {1} {2}° (feels like {3}°)'.format(icon, current.summary, round(current.temperature), round(current.apparentTemperature))

  if application.config['DEBUG']:
    print(post)
  else:
    bot.post(post)

@command('!gif')
def gif(bot, message, author=None):
  img = giphypop.translate(phrase=message, strict=True)

  if application.config['DEBUG']:
    print(img.media_url)
  else:
    bot.post(img.media_url)

@command('!slap')
def slap(bot, message, author=None):
  if author is None:
    return

  slap = '{0} slaps {1} around a bit with a large trout'.format(author, message)

  if application.config['DEBUG']:
    print(slap)
  else:
    bot.post(slap)

@command('!foo')
def foo(bot, message, author=None):
  print('foo', message)

@application.route('/pancakebot', methods=['POST'])
def hello():
  data = request.get_json()
  bot = groupy.Bot.list().first

  user = data['name']
  message = data['text']

  print('Received message: {0}'.format(data))

  for command in commands:
    if not message.startswith(command + ' ') and message != command:
      continue

    print('Executing command: {0}'.format(command))

    for callback in commands[command]:
      try:
        callback(bot, message[len(command):].strip(), author=user)
      except Exception as e:
        print('Error executing command: {0}'.format(command))
        print(e)

  return 'OK'

if __name__ == '__main__':
  application.run(host='0.0.0.0', port=5555)
