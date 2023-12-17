import os
import telebot
from bs4 import BeautifulSoup
import requests

bot_token = "6818823640:AAEdl1JN86rcyTpXVR7doOyaBjI9DOSOPHA"
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Отправляет приветственное сообщение пользователю и инструкцию по получению погоды.

    Args:
        message (telebot.types.Message): Объект сообщения, который вызвал функцию.

    Returns:
        None
    """
    bot.reply_to(message, "Hello! Send me the message '/weather' to get the weather for your city.")

@bot.message_handler(func=lambda message: message.text == '/weather')
def send_weather(message):
    """
    Отправляет данные о погоде пользователю на основе его местоположения.

    Args:
        message (telebot.types.Message): Объект сообщения, который вызвал функцию.

    Returns:
        None
    """
    # Get user's city using their IP address
    ip_data = requests.get('http://ip-api.com/json/').json()
    city = ip_data['city']

    # Scrape weather data for user's city
    url = f'https://www.google.com/search?q=weather+{city}'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

    data = str.split('\n')
    time = data[0]
    sky = data[1]
    # Send weather data to user
    bot.send_message(message.chat.id, f'City: {city}\nTemperature: {temp}\nTime: {time}\nSky: {sky}')

bot.polling()
