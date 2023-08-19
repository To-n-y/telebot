import datetime
import requests
import telebot

from bs4 import BeautifulSoup as bs
from telebot import types

from config import URL, API_TOKEN

bot = telebot.TeleBot(API_TOKEN)


def parser(fl):  # 1 - yesterday 2 - now 3 - tomorrow
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )
    response = requests.get(URL, headers=headers)
    soup = bs(response.text, "html.parser")

    now_date = soup.findAll('div', class_='now-localdate')[0].get_text()
    now_desc = soup.findAll('div', class_='now-desc')[0].get_text()

    MainInfo = soup.findAll('span', class_='unit unit_temperature_c')
    temp_now = MainInfo[0].get_text()
    temp_feel_like = MainInfo[1].get_text()

    wind = soup.findAll('div', class_='unit unit_wind_m_s')[0].get_text().replace('м/c', ' м/с ')
    pressure = soup.findAll('div', class_='unit unit_pressure_mm_hg_atm')[0].get_text().replace('ммрт. ст.', '')
    humidity = soup.findAll('div', class_='now-info-item humidity')[0].get_text().replace('Влажность', '')
    gm = soup.findAll('div', class_='now-info-item gm')[0].get_text().replace('Г/м активность', '').replace('баллаиз 9',
                                                                                                            '')
    water = soup.findAll('div', class_='now-info-item water')[0].get_text().split()[0].replace('Вода', '')

    sun = soup.findAll('div', class_='time')
    sun_rise = sun[0].get_text()
    sun_set = sun[1].get_text()

    answer = now_date + "\n" + now_desc + "\nТемпература сейчас: " + temp_now + "\nПо ощущению: " + temp_feel_like + "\nВетер: " + wind + "\nДавление: " + pressure + "мм рт.ст.\nВлажность: " + humidity + "\nГеомагнитная активность: " + gm + " из 9\nВода: " + water + "\nВосход был: " + sun_rise + "\nЗакат: " + sun_set
    print(answer)
    return answer


parser(1)


@bot.message_handler(commands=['start'])
def start(message):
    # TODO: logger
    with open("log.txt", "a") as log:
        log.write("Имя: " + message.from_user.first_name + " id: " + str(message.from_user.id) + " Приветствие ")
        log.write(str(datetime.datetime.now()))
        log.write('\n')

    print(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("❓ Узнать погоду сейчас")
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
    elif message.text == "❓ Узнать погоду сейчас":
        answer_now = parser(2)
        bot.send_message(message.chat.id, text=answer_now)
    elif message.text == "❓ Узнать погоду завтра":
        pass
    else:
        pass

bot.polling()
