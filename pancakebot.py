import logging
from logging.handlers import RotatingFileHandler
import groupy
from flask import Flask, request

application = Flask(__name__)

@application.route('/pancakebot', methods=['POST'])
def hello():
  data = request.get_json()
  print(data)
  bot = groupy.Bot.list().first
  
  user = data['name']
  message = data['text']  
  
  if 'aaron' in message.lower() and user != 'pancakebot':
    bot.post('Is someone talking shit about Aaron? I will fight you.')

  return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
  application.run(host='0.0.0.0', port='5555')
