from distutils.dist import command_re
from email import message_from_bytes
from gc import callbacks

import requests
from io import BytesIO
from PIL import Image

from deep_translator import GoogleTranslator

import random
import datetime
import time
import datetime
import telebot
import webbrowser
from telebot import types
import sqlite3

name = ''
c = 0
tren = 0
nomer_tren = 0
bot = telebot.TeleBot("7638727063:AAGiN1lA5SDPYwwLt3EnYGEwGiE62pONLkg")
bb = 0
kartinki = 0

HF_API_KEY = "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"
MODEL_NAME = "stabilityai/stable-diffusion-xl-base-1.0"


p = ["Нужно больше спать...", "Язык мой – враг мой", "Даже солнце не всем одинаково светит", "Не руби сук на котором сидишь", "Большому кораблю, большое плавание", "Лучше синица в руках, чем журавль в небе", "Скоро сказка сказывается, да не скоро дело делается", "Хороша Маша, да не наша"]

@bot.message_handler(commands=['logovo'])
def main(mas):
    a = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Смотреть на панд')
    btn2 = types.KeyboardButton('Кормить панду',)
    btn3 = types.KeyboardButton('Купать панду')
    btn4 = types.KeyboardButton('Тренировка')
    a.row(btn2, btn3)
    a.row(btn4)
    a.row(btn1)
    f_panda = open('./panda.jpg', 'rb')  # Открытие файла на чтение rb
    bot.send_photo(mas.chat.id, f_panda, reply_markup=a)
    bot.send_message(mas.chat.id, f'Ты в логове. Слышишь, как растёт бамбук?', reply_markup=a)

    bot.register_next_step_handler(mas, on_click)

def on_click(mas):
    global kartinki
    if mas.text.lower() == 'смотреть на панд':
        kartinki = 1
        bot.send_message(mas.chat.id, 'Смотри, какие милашки: https://yandex.ru/images/search?from=tabbar&text=картинки%20панды  /logovo')
        bot.send_message(mas.chat.id, f'Поблизости ходит большое количество панд. Какую панду ты бы хотел увидеть?')

    elif mas.text.lower() == 'кормить панду':

        bot.send_message(mas.chat.id, 'Подожди чуток. Твоя панда ест...')
        time = 0
        conn = sqlite3.connect('power_panda.sql')
        cur = conn.cursor()

        id = mas.from_user.id
        cur.execute(f"SELECT * FROM users WHERE idTG = {id}")

        el = cur.fetchone()
        t1 = el[4]
        t2 = datetime.datetime.now().timestamp()
        cur.execute(f"UPDATE users SET eat = '{t2}' WHERE idTG = {id}")
        t = (t2 - t1)//1

        conn.commit()
        cur.close()
        conn.close()

        bot.send_photo(mas.chat.id, open('./eat.png', 'rb'))
        bot.send_message(mas.chat.id, f'Ты покормил свою панду! До этого момента она не ела целых {t} секунд! /logovo')
        main(mas)
    elif mas.text.lower() == 'купать панду':
        bot.send_photo(mas.chat.id, open('./vanna.webp', 'rb'))
        prasa = p[random.randint(0,len(p)-1)]
        bot.send_message(mas.chat.id, f'Буль-буль! Ты искупал свою панду! Ты знаешь, после купания панд всегда тянет на философию. И твоя сегодня поймала филосовскую волну, она шепчет тебе:"{prasa}" /logovo')
        main(mas)
    elif mas.text.lower() == 'тренировка':

        conn = sqlite3.connect('power_panda.sql')
        cur = conn.cursor()

        id = mas.from_user.id
        cur.execute(f"SELECT * FROM users WHERE idTG = {id}")

        el = cur.fetchone()
        power = el[3]
        panda = el[2]
        t = el[4]
        conn.commit()
        cur.close()
        conn.close()

        a = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Да! Долгая тренировка', callback_data='long')
        btn2 = types.InlineKeyboardButton('Да! Быстрая тренировка', callback_data='short')  # Вызов функции с таким названием
        btn3 = types.InlineKeyboardButton('В другой раз...',
                                          callback_data='logovo')
        a.row(btn1)
        a.row(btn2)
        a.row(btn3)

        bot.send_photo(mas.chat.id, open('./tren.webp', 'rb'))
        bot.send_message(mas.chat.id, f'Сила твоей панды измеряется в кол-ве палочек бамбука, которые она может поднять за один раз. Сейчас сила {panda} составляет {power} палочек. Хочешь начать тренировку?', reply_markup=a)


@bot.message_handler(commands=['start'])
def start(mes):
    conn = sqlite3.connect('power_panda.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(50), panda varchar(50), power INTEGER, eat INTEGER, idTG INTEGER)') #Айди (целое число, самоизменяющаяся строка)
    conn.commit() #соединяет, синхронизирует с файлом

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    est = 0
    for el in users:
        if el[5] == mes.from_user.id:
            est = 1
    if est == 1:
        print(f'Я вижу, {el[1]}, у тебя уже есть <em><u>ПАВЕР</u>панда</em> по имени {el[2]}. Напиши в чат /logovo', parse_mode="html")
    else:
        p1 = open('./p1.jpg', 'rb')
        bot.send_photo(mes.chat.id, p1)
        bot.send_message(mes.chat.id, f'Ва-ха-ха! Привет! Ты пришёл чтобы забрать свою <em><u>ПАВЕР</u></em>панду? Этим крохам нужна твоя забота... Я рад, что ты готов им её дать. Представься же, добрый путник! <em>Введи своё имя</em>', parse_mode='html')
        bot.register_next_step_handler(mes, user_name)

    cur.close()  # закрывает соединение
    conn.close()
def user_name(mes):
    global name
    name = mes.text.strip()   #strip удаляет пробелы
    p2 = open('./p2.jpg', 'rb')
    bot.send_photo(mes.chat.id, p2)
    bot.send_message(mes.chat.id,
                     f'Приятно познакомиться, {name}! Как ты назовёшь свою <em><u>ПАВЕР</u>панду</em>???', parse_mode='html')
    bot.register_next_step_handler(mes, panda_name)
def panda_name(mes):
    panda = mes.text.strip()   #strip удаляет пробелы

    time = datetime.datetime.now().timestamp()

    conn = sqlite3.connect('power_panda.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, panda, eat, idTG, power) VALUES ('%s', '%s', '%s', '%s', '%s')" % (name, panda, time, mes.from_user.id, 0))
    conn.commit()
    cur.close()
    conn.close()

    a = types.InlineKeyboardMarkup()
    a.add(types.InlineKeyboardButton('Все существующие панды', callback_data='pandi'))
    yp = open('./your panda.jpg', 'rb')
    bot.send_photo(mes.chat.id, yp)
    bot.send_message(mes.chat.id,
                     f'{panda}? {panda}! Замечательно))', parse_mode='html', reply_markup=a)
    #bot.register_next_step_handler(mes, panda_name)

@bot.callback_query_handler(func=lambda call: True)
def cb(call):
    global tren, c, nomer_tren, bb
    if call.data == 'pandi':
        conn = sqlite3.connect('power_panda.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        info = ('')
        for el in users:
            info += f'<em><u>ПАВЕР</u>панда</em> {el[2]} с хозяином {el[1]}\n'  #\n на новую строку перевод

        #conn.commit()
        cur.close()
        conn.close()

        spisok = open('./spisok.jpg', 'rb')
        bot.send_photo(call.message.chat.id, spisok)

        bot.send_message(call.message.chat.id, info, parse_mode='html')
        bot.send_message(call.message.chat.id, "Теперь ты можешь попать в логово - место где живёт твоя панда. Там ты сможешь кормить, купать и тренировать свою панду. Напиши в чат /logovo")
    elif call.data == 'logovo':
        bot.send_message(call.message.chat.id, 'Возвращайся, как только будешь готов прокачать свою <em><u>ПАВЕР</u>панду</em>!!!', parse_mode='html')
        main(call.message)
        tren = 1
        nomer_tren = 0
    elif call.data == 'long':
        mas = call.message
        bot.send_message(mas.chat.id, 'Сейчас начнётся сложная тренировка. У тебя будет минута для того чтобы дать ответы на все примеры. Удачи!)')
        bb = 25
        b = random.randint(2, bb)
        a = random.randint(2, bb)
        c = a * b
        bot.reply_to(mas, f'Сколько будет {a} х {b}?')

        tren = 1
        time.sleep(60)
        tren = 0

        bot.send_message(mas.chat.id,
                             f'Вы с пандой большие молодцы! Вы прошли через сложную тренниновку. Ты прокачиваешь свою панду на {nomer_tren} палочек. Возвращайся в логово /logovo')

        conn = sqlite3.connect('power_panda.sql')
        cur = conn.cursor()

        id = mas.from_user.id
        cur.execute(f"SELECT * FROM users WHERE idTG = {id}")
        el = cur.fetchone()
        t1 = el[3]
        t2 = t1 + nomer_tren // 2
        cur.execute(f"UPDATE users SET power = '{t2}' WHERE idTG = {id}")

        conn.commit()
        cur.close()
        conn.close()

        nomer_tren = 0
        main(mas)
    elif call.data == 'short':
        mas = call.message
        bot.send_message(mas.chat.id,
                         'Сейчас начнётся короткая тренировка. У тебя будет 30 секунд для того чтобы дать ответы на все примеры. Удачи!)')
        bb = 12
        b = random.randint(2, bb)
        a = random.randint(2, bb)
        c = a * b
        bot.reply_to(mas, f'Сколько будет {a} х {b}?')

        tren = 1
        time.sleep(30)
        tren = 0

        bot.send_message(mas.chat.id,
                         f'Вы с пандой большие молодцы! Вы прошли через сложную тренниновку. Ты прокачиваешь свою панду на {nomer_tren//2} палочек. Возвращайся в логово /logovo')
        main(mas)

        conn = sqlite3.connect('power_panda.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE idTG = ?", (call.from_user.id,))
        el = cur.fetchone()
        t1 = el[3]
        t2 = t1 + nomer_tren//2
        cur.execute(f"UPDATE users SET power = '{t2}' WHERE idTG = {call.from_user.id}")

        conn.commit()
        cur.close()
        conn.close()

        nomer_tren = 0

@bot.message_handler(content_types=["text"])
def treni(mas):
    global c, tren, nomer_tren, kartinki, HF_API_KEY, MODEL_NAME
    if tren != 0:
        panda = mas.text.strip()
        if int(panda) != c:
            bot.send_message(mas.chat.id,
                             f'Ты не прав! Увы:( Попробуй ещё раз, но перед этим возвращайся в логово /logovo')
            tren = 0 #Оборвалась
        b = random.randint(2, bb)
        a = random.randint(2, bb)
        c = a * b
        nomer_tren += 1
        bot.reply_to(mas, f'Сколько будет {a} х {b}?')
    if kartinki != 0:
        prompt = translate_to_english("Панда " + mas.text)

        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        api_url = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

        try:
            # Отправка запроса
            response = requests.post(
                api_url,
                headers=headers,
                json={"inputs": prompt}
            )

            # Обработка ответа
            if response.status_code == 200:
                # Конвертируем бинарные данные в изображение
                image = Image.open(BytesIO(response.content))

                # Сохраняем временный файл
                image_path = "generated_image.png"
                image.save(image_path)

                # Отправляем фото
                with open(image_path, 'rb') as photo:
                    bot.send_photo(mas.chat.id, photo, caption=f"🖼 Вот, что ты увидел сегодня. Скорее возвращайся в логово! /logovo")
            else:
                error = response.json().get("error", "Unknown error")
                bot.reply_to(mas, f"❌ Ошибка: {error} (Код: {response.status_code})")

        except Exception as e:
            bot.reply_to(mas, f"🔥 Ошибка: {str(e)}")


        kartinki = 0

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text

@bot.message_handler(commands=['help'])
def help(mas):
    m = str(mas)
    m1 = m[:len(m)//2]
    m2 = m[len(m) // 2:len(m)]
    bot.send_message(mas.chat.id, m1)
    bot.send_message(mas.chat.id, m2)

def logovo(chat_id):
    """Отображает клавиатуру логова"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # ... создание кнопок
    btn1 = types.KeyboardButton('Смотреть на панд')
    btn2 = types.KeyboardButton('Кормить панду', )
    btn3 = types.KeyboardButton('Купать панду')
    btn4 = types.KeyboardButton('Тренировка')
    a.row(btn2, btn3)
    a.row(btn4)
    a.row(btn1)
    #
    bot.send_photo(chat_id, open('./panda.jpg', 'rb'),
                  caption='Ты в логове. Слышишь как растёт бамбук?',
                  reply_markup=markup)

bot.polling(none_stop=True)