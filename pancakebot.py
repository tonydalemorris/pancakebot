import logging
from logging.handlers import RotatingFileHandler

import groupy
import forecastio
import giphypop
import requests
import bs4
from geopy.geocoders import Nominatim
from flask import Flask, request

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
def weather(bot, message, author=None, debug=False):
  api_key = application.config['FORECASTIO_API_KEY']

  if api_key is None:
    print('FORECASTIO_API_KEY not configured, not displaying weather information!')

  geolocator = Nominatim()
  location = geolocator.geocode(message or 'Austin, TX')
  forecast = forecastio.load_forecast(api_key, location.latitude, location.longitude)
  current = forecast.currently()
  icon = WEATHER_ICONS[current.icon] or ''

  post = '{0}  {1} {2}° (feels like {3}°)'.format(icon, current.summary, round(current.temperature), round(current.apparentTemperature))

  if debug:
    print(post)
  else:
    bot.post(post)

@command('!gif')
def gif(bot, message, author=None, debug=False):
  img = giphypop.translate(phrase=message, strict=True)

  if debug:
    print(img.media_url)
  else:
    bot.post(img.media_url)

@command('!slap')
def slap(bot, message, author=None, debug=False):
  if author is None:
    return

  slap = '{0} slaps {1} around a bit with a large trout'.format(author, message)

  if debug:
    print(slap)
  else:
    bot.post(slap)

@command('!h')
def horoscope(bot, message, author=None, debug=False):
  sign = message.lower()

  signs = [
    'aries',
    'taurus',
    'gemini',
    'cancer',
    'leo',
    'virgo',
    'libra',
    'scorpio',
    'sagittarius',
    'capricorn',
    'aquarius',
    'pisces'
  ]

  if sign not in signs:
    error = '{0} is not a star sign, zodiac thing, or whatever.'.format(message)
    if debug:
      print(error)
    else:
      bot.post()
    return

  url = 'http://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={0}'.format(signs.index(sign) + 1)
  page = requests.get(url)

  soup = bs4.BeautifulSoup(page.content, 'lxml')
  elements = soup.select('.block-horoscope-text')
  if len(elements) == 0:
    print('Unable to find horoscope for: {0}'.format(message))
    return
  horoscope = '{0}: {1}'.format(message, elements[0].getText().strip())
  if debug:
    print(horoscope)
  else:
    bot.post(horoscope)

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
        callback(bot, message[len(command):].strip(), author=user, debug=application.config['DEBUG'])
      except Exception as e:
        print('Error executing command: {0}'.format(command))
        print(e)

  return 'OK'

if __name__ == '__main__':
  application.run(host='0.0.0.0', port=5555)
