import datetime
import requests
import telebot
import os

from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
from telebot import types

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

URL = os.getenv("URL", "secret")
API_TOKEN = os.getenv("API_TOKEN", "secret")

bot = telebot.TeleBot(API_TOKEN)


def parser(fl):  # 1 - yesterday 2 - today 3 - tomorrow
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )
    response = requests.get(URL, headers=headers)
    soup = bs(response.text, "html.parser")
    MainInfo = soup.findAll('span', class_='unit unit_temperature_c')
    temp_now = MainInfo[0].get_text()
    temp_feel_like = MainInfo[1].get_text()
    print(temp_now, temp_feel_like, len(MainInfo))
    wind = soup.findAll('div', class_='unit unit_wind_m_s')[0].get_text().replace('м/c', ' м/с ')
    pressure = soup.findAll('div', class_='unit unit_pressure_mm_hg_atm')[0].get_text().replace('ммрт. ст.', '')
    humidity = soup.findAll('div', class_='now-info-item humidity')[0].get_text().replace('Влажность', '')
    gm = soup.findAll('div', class_='now-info-item gm')[0].get_text().replace('Г/м активность', '').replace('баллаиз 9',
                                                                                                            '')
    water = soup.findAll('div', class_='now-info-item water')[0].get_text().split()[0].replace('Вода', '')
    print(wind, pressure, humidity, gm, water, sep='\n')

    sun_set_rise = soup.findAll('div', class_='time')[0].get_text()

    now_date = soup.findAll('div', class_='now-localdate')[0].get_text()


parser(1)


@bot.message_handler(commands=['start'])
def start(message):
    # TODO: loger
    with open("log.txt", "a") as log:
        log.write("Имя: " + message.from_user.first_name + " id: " + str(message.from_user.id) + " Приветствие ")
        log.write(str(datetime.datetime.now()))
        log.write('\n')

    print(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("❓ Узнать погоду сегодня")
    btn2 = types.KeyboardButton("❓ Узнать погоду завтра")
    btn3 = types.KeyboardButton("❓ Узнать погоду вчера")
    btn4 = types.KeyboardButton("👋 TODO")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я тестовый бот для твоей мамы".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == "❓ Узнать погоду вчера":
        pass
    elif message.text == "❓ Узнать погоду сегодня":
        pass
    elif message.text == "❓ Узнать погоду завтра":
        pass
    else:
        pass

# bot.polling()
