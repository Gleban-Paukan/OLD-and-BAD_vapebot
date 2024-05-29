#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os
import sys
import time as tm

import qrcode
import telebot
from requests import ReadTimeout
from telebot import types

import InfoUser
import support_library

bot = telebot.TeleBot('')
bot.parse_mode = 'html'
admins = []
balance_dict = {}


@bot.message_handler(commands=['start'])
def welcome(message):
    with open('UsersInfo.txt', 'r') as file:
        Users = [x.split()[0] for x in file]
    if ' ' in message.text and message.chat.id in admins:
        buyer = InfoUser.DefineUser(message.chat.id)
        bot.send_message(message.chat.id,
                         f'Нашёл пользователя <ins>{buyer.name}</ins>, его номер телефона <ins>{buyer.phone}</ins>\n\nВведите, сколько баллов ему начислить.')
        balance_dict[message.chat.id] = int(message.text.split()[1])
        bot.register_next_step_handler(message, add_coins)
    elif str(message.chat.id) in Users:
        user = InfoUser.DefineUser(message.chat.id)
        bot.send_message(message.chat.id,
                         f"Привет, <b>{user.name}</b> 😍, твой баланс {user.balance}, последний раз мы тебя видели {support_library.define_date(user.date)}, сейчас у тебя скидка <b>{int((1 - support_library.define_sale_procent(user.balance)) * 100)}%</b>.\n{support_library.define_left_for_sale(user.balance)}")
    else:
        with open('UsersId.txt', 'a') as file:
            file.write(f'{message.chat.id}\n')
        for _ in range(3):
            bot.send_chat_action(message.chat.id, 'typing')
            tm.sleep(.5)
        bot.send_message(message.chat.id, 'Привет! Спасибо, что доверяешь нашему <b>шопу</b> ❤️')
        for _ in range(6):
            bot.send_chat_action(message.chat.id, 'typing')
            tm.sleep(.5)
        bot.send_message(message.chat.id,
                         '''GRADE SHOP BONUS РАБОТАЕТ ТАК👇
<b>
Как только твой счет покажет: 
3 000 баллов, твоя скидка составит 2%
5 000 баллов, твоя скидка составит 3%
7 000 баллов, твоя скидка составит 5%
</b>
Все просто, чем больше покупаешь, тем больше процент скидки. Скидка распространяется на весь ассортимент товаров в нашем магазине🔥
''')
        for _ in range(16):
            bot.send_chat_action(message.chat.id, 'typing')
            tm.sleep(.5)
        bot.send_message(message.chat.id,
                         '''Баллы обновляются и сгорают каждый месяц. Например, если на вашем счету <b>3 000 
                         баллов</b>, (а это 2% скидки) то скидка действует ровно 1 месяц с момента ее получения.

<b>Чтобы не потерять скидку, поддерживайте уровень баллов 😏</b>''')
        for _ in range(12):
            bot.send_chat_action(message.chat.id, 'typing')
            tm.sleep(.5)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(callback_data='registration', text='ЗАРЕГИСТРИРОВАТЬСЯ 🔥'))
        bot.send_message(message.chat.id, 'Зачислить на твой аккаунт <b>500 баллов</b>? ☄️', reply_markup=markup)


@bot.message_handler(commands=['account'])
def account(message):
    user = InfoUser.DefineUser(message.chat.id)
    if user.ID != None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Изменить имя', 'Изменить номер телефона')
        bot.send_message(message.chat.id, f'Мои данные 🫶\n\n<b>Имя:</b> {user.name}\n<b>Телефон</b>: {user.phone}',
                         reply_markup=markup)
        send_QR(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, зарегистрируйтесь, чтобы пользоваться ботом.')


@bot.message_handler(commands=['scores'])
def scores(message):
    user = InfoUser.DefineUser(message.chat.id)
    if user.ID != None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton('Показать QR для начисления'))
        bot.send_message(message.chat.id,
                         f'{user.name}, у тебя <b>{user.balance} баллов</b>, твоя скидка составляет {int((1 - support_library.define_sale_procent(user.balance)) * 100)}%.',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, зарегистрируйтесь, чтобы пользоваться ботом.')


@bot.message_handler(commands=['faq'])
def scores(message):
    bot.send_message(message.chat.id, 'Задай вопрос в нашем чате: <b>https://t.me/LINK_IS_PRIVATE</b>')


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Показать QR для начисления':
            send_QR(message)
        elif message.text == 'Запуск':
            while True:
                checker_date()
                tm.sleep(60 * 60 * 12)  # Yes, I know :) I was too young
        elif message.text == 'Изменить имя':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton('Отмена'))
            bot.send_message(message.chat.id, 'Введите новое имя', reply_markup=markup)
            bot.register_next_step_handler(message, change_name)
        elif message.text == 'Изменить номер телефона':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton('Отмена'))
            bot.send_message(message.chat.id, 'Введите новый номер телефона в формате <b>+79xxxxxxxxx</b>',
                             reply_markup=markup)
            bot.register_next_step_handler(message, change_phone)


@bot.message_handler(content_types=['left_chat_member'])
def leave_memb(message):
    bot.delete_message(message.chat.id, message.id)


@bot.message_handler(content_types=['new_chat_members'])
def qweqwewq(message):
    bot.delete_message(message.chat.id, message.id)
    msg = bot.send_message(message.chat.id,
                           f'<ins><i>{message.from_user.first_name}</i></ins>, приветствуем вас в нашем сообществе!',
                           parse_mode='html')
    tm.sleep(60)
    bot.delete_message(msg.chat.id, msg.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'registration':
            for _ in range(3):
                bot.send_chat_action(call.message.chat.id, 'typing')
                tm.sleep(.5)
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton('✅ Принять', callback_data='accept_politics'))
            bot.send_message(call.message.chat.id,
                             '''Для продолжения необходимо внимательно ознакомиться с <b><a 
                             href="https://docs.google.com/document/d/LINK_IS_PRIVATE/edit?usp=sharing">политикой 
                             конфиденциальности</a></b> и, если согласны, то нажать <b>"✅ Принять"</b>''',
                             reply_markup=markup, disable_web_page_preview=True)
        elif call.data == 'accept_politics':
            for _ in range(3):
                bot.send_chat_action(call.message.chat.id, 'typing')
                tm.sleep(.5)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(text='Поделиться контактом 📤', request_contact=True))
            bot.send_message(call.message.chat.id, 'Поделитесь номером телеграмм', reply_markup=markup)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.message_handler(content_types=['contact'])
def accept_phone(message):
    if message.contact is not None:
        with open('UsersPhone.txt', 'a') as users_id:
            users_id.write(str(message.chat.id) + f' {str(message.contact.phone_number)}\n')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for _ in range(2):
            bot.send_chat_action(message.chat.id, 'typing')
            tm.sleep(.5)
        bot.send_message(message.chat.id, 'Хорошо, теперь введите ваше имя', reply_markup=markup)
        bot.register_next_step_handler(message, user_name)


def user_name(message):
    if (' ' not in message.text) and len(message.text) <= 30 and message.text.isalpha():
        with open('UsersName.txt', 'a') as users_id:
            users_id.write(str(message.chat.id) + f' {message.text}\n')
        for _ in range(3):
            bot.send_chat_action(message.chat.id, 'typing')
            tm.sleep(.5)
        bot.send_message(message.chat.id, 'Отлично! Теперь пришли дату рождения в формате <b>дд.мм.гггг</b>')
        bot.register_next_step_handler(message, user_birthday)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введи только своё имя.')
        bot.register_next_step_handler(message, user_name)


def user_birthday(message):
    try:
        s = message.text.split('.')
        dt = datetime.date(int(s[2]), int(s[1]), int(s[0]))
        years = (datetime.date.today() - dt).days // 364
        if years >= 18:
            with open('UsersInfo.txt', 'a', encoding='utf-8') as file:
                with open('UsersName.txt', 'r', encoding='utf-8') as f:
                    for x in f:
                        if str(message.chat.id) in x:
                            name = x.split()[1]
                            break
                with open('UsersPhone.txt', 'r') as f:
                    for x in f:
                        if str(message.chat.id) in x:
                            phone = x.split()[1]
                            break
                file.write(str(message.chat.id) + f' {name},{phone},500,{datetime.date.today()},0\n')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Показать QR для начисления'))
            for _ in range(2):
                bot.send_chat_action(message.chat.id, 'typing')
                tm.sleep(.5)
            bot.send_message(message.chat.id,
                             f'Поздравляю тебя, <b>{name}</b>!😍 На твой счёт зачислено <b>500 баллов</b>.',
                             reply_markup=markup)
            for _ in range(1):
                bot.send_chat_action(message.chat.id, 'typing')
                tm.sleep(.5)
            send_QR(message)
        else:
            bot.send_message(message.chat.id, 'Вам нет 18 лет. Попробуйте ещё раз.')
            bot.register_next_step_handler(message, user_birthday)
    except Exception as Ex:
        print(Ex)
        bot.send_message(message.chat.id, 'Пожалуйста, напиши свою дату рождения в формате <b>дд.мм.гггг</b>')
        bot.register_next_step_handler(message, user_birthday)


def send_QR(message):
    qrcode.make(f'https://t.me/LINK_IS_PRIVATE?start={message.chat.id}').save('QR.png')
    with open('QR.png', 'rb') as QR:
        bot.send_photo(message.chat.id, photo=QR,
                       caption='Твой QR код для начисления баллов, покажи его продавцам при оплате для начисления баллов')
    os.remove('QR.png')


def add_coins(message):
    if message.text[1:].isdigit():
        support_library.add_balance(balance_dict[message.chat.id], int(message.text))
        user = InfoUser.DefineUser(balance_dict[message.chat.id])
        bot.send_message(message.chat.id,
                         f'Баланс пользователя пополнил. Теперь его баланс {user.balance}.\nСейчас его скидка {int((1 - support_library.define_sale_procent(user.balance - int(message.text))) * 100)}%, его чек составит {int(message.text) * support_library.define_sale_procent(user.balance - int(message.text))}')
        bot.send_message(user.ID, f'''
Совершая покупки у нас, ты становишься счастливее❤️ 
Твои баллы за покупку на <b>{message.text} рублей</b>, баланс составляет <b>{user.balance} баллов</b> 
''')


def checker_date():
    with open('UsersInfo.txt', 'r') as file:
        for i in file:
            user = InfoUser.DefineUser(i.split()[0])
            x = user.date.split('-')
            past_days = (datetime.date.today() - datetime.date(int(x[0]), int(x[1]), int(x[2]))).days
            if 14 <= past_days <= 30 and user.flag == 0:
                bot.send_message(user.ID,
                                 f'Привет, ну как твои дела?\n<b>{user.name}</b>, давно тебя не видели, ждём в гости 😍')
                support_library.change_flag(user.ID, 1)
            elif past_days > 30:
                support_library.add_balance(user.ID, -1 * user.balance)
                bot.send_message(user.ID,
                                 'Привет. Ты не был у нас более 30 дней. К сожалению, по правилам проргаммы лояльности пришлось обнулить баланс.')


def change_name(message):
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Действие <b>отменено.</b>')
    else:
        if (' ' not in message.text) and len(message.text) <= 30 and message.text.isalpha():
            support_library.change_data(message.chat.id, new_name=message.text)
            bot.send_message(message.chat.id, 'Имя изменено.')
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton('Отмена'))
            bot.send_message(message.chat.id, 'Пожалуйста, введи только своё имя.', reply_markup=markup)
            bot.register_next_step_handler(message, change_name)


def change_phone(message):
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Действие <b>отменено.</b>')
    else:
        if message.text[0] == '+' and message.text[1:].isdigit() and len(message.text) == 12:
            support_library.change_data(message.chat.id, new_phone=message.text)
            bot.send_message(message.chat.id, 'Номер изменён')
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton('Отмена'))
            bot.send_message(message.chat.id, 'Пожалуйста, введите номер телефона в формате <b>+79xxxxxxxxx</b>',
                             reply_markup=markup)
            bot.register_next_step_handler(message, change_name)


try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
