from dotenv import load_dotenv
import os
import webbrowser
import telebot
import requests
import json
import datetime
from telebot import types
import sqlite3

# нужно как-то хранить переменную city именно на этом месте для использования функции get_weather и get_places
# и нужно понять, как эту переменную закидывать в функции

load_dotenv
API = os.getenv('dedd8faab24bf4b5adb455980850dc90')
bot = telebot.Telebot('7181902570:AAGkf7jrLqvhN-pJgvL6NGQr_vE3F1NYTg0')

@bot.message_handler(commands=['start'])
def start(message):
    file = open('./video.MP4', 'rb')
    bot.send_video(message.chat.id, file)
    # начало переписки чата с приветствия
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! 🏖🤘')
    bot.send_message(message.chat.id, 'Рад тебя видеть! Напиши название города')



@bot.message_handler(content_types=['text'])
# def get_place(message):
#     global city
#     city = message.text.strip().lower()
#
#
#
#
#
#     bot.register_next_step_handler(message, get_weather)


def get_weather(message):
    # city = message.text.strip().lower()

    # url = f'https://ru.wikipedia.org/w/api.php?action=query&list=search&srsearch=достопримечательности+в+{city}&format=json'
    #
    # response = requests.get(url)
    # data = response.json()
    #
    # # Создание списка достопримечательностей с нумерацией
    # attractions = [(index + 1, item['title']) for index, item in enumerate(data['query']['search'])]
    #
    # # Вывод списка достопримечательностей с нумерацией
    # for attraction in attractions:
    #     bot.send_message(message.chat.id, f"{attraction[0]}. {attraction[1]}")
    #
    # # Предоставление выбора клиенту
    # bot.send_message(message.chat.id, "Выберите номер достопримечательности для получения подробной информации: ")
    # selected_attraction = message.text.strip().lower()
    # selected_attraction = int(selected_attraction)
    # selected_title = attractions[selected_attraction - 1][1]
    #
    # bot.send_message(message.chat.id, f"Вы выбрали достопримечательность: {selected_title}")

    city = message.text.strip().lower()

    url = f'https://ru.wikipedia.org/w/api.php?action=query&list=search&srsearch=достопримечательности+в+{city}&format=json'

    response = requests.get(url)
    data = response.json()

    # Создание списка достопримечательностей с нумерацией
    attractions = [(index + 1, item['title']) for index, item in enumerate(data['query']['search'])]

    # Отправка списка достопримечательностей с нумерацией через Telegram бот
    attractions_message = "\n".join([f"{attraction[0]}. {attraction[1]}" for attraction in attractions])
    bot.send_message(message.chat.id, attractions_message)

    # Флаг для хранения состояния ожидания выбора достопримечательности
    state = "waiting_for_selection"

    @bot.message_handler(func=lambda message: state == "waiting_for_selection")
    def handle_selection(message):
        try:
            selected_attraction = int(message.text)
            selected_title = attractions[selected_attraction - 1][1]
            bot.send_message(message.chat.id, f"Вы выбрали достопримечательность: {selected_title}")

            # Сброс состояния ожидания
            state = "default"
        except:
            bot.send_message(message.chat.id, "Пожалуйста, введите правильный номер достопримечательности.")

    #
    # res = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API}&units=metric')
    # if res.status_code == 200:
    #     #data = json.loads(res.text)
    #
    #     # Преобразуем ответ в JSON
    #     data = res.json()
    #
    #     # Получаем текущую дату
    #     current_date = datetime.datetime.now().date()
    #
    #     # Инициализируем переменные для хранения данных о погоде
    #     forecast_data = []
    #
    # # Обрабатываем данные из ответа
    #     for item in data["list"]:
    #         # Извлекаем дату из времени
    #         forecast_date = datetime.datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").date()
    #
    #         # Проверяем, является ли дата следующим днем и время 12:00:00
    #         if forecast_date > current_date and item["dt_txt"].endswith("12:00:00"):
    #             # Извлекаем температуру
    #             temperature = item["main"]["temp"]
    #
    #             # Извлекаем тип погоды
    #             weather_type = item["weather"][0]["main"]
    #
    #             # Добавляем данные в список
    #             forecast_data.append({
    #                 "date": forecast_date,
    #                 "temperature": temperature,
    #                 "weather_type": weather_type
    #             })
    #
    #
    #
    #     # Выводим полученные данные
    #     if forecast_data:
    #         for data in forecast_data:
    #             if data["weather_type"] == 'Clouds':
    #                 emojy = '☁️'
    #             elif data["weather_type"] == 'Sunny' or data["weather_type"] == 'Clear':
    #                 emojy = '☀️'
    #             elif data["weather_type"] == 'Rain':
    #                 emojy = '🌧'
    #             elif data["weather_type"] == 'Snow':
    #                 emojy = '🌨'
    #             bot.reply_to(message,f"Погода на {data["date"]}\nТемпература: {data["temperature"]} °C\nТип погоды: {data["weather_type"]}")
    #             bot.send_message(message.chat.id, emojy)
    #
    # else:
    #     bot.reply_to(message, 'Город указан не верно')
    #
    #
    #





bot.polling(none_stop=True)