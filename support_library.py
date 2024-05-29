# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime


def add_balance(ID, coins):
    with open('UsersInfo.txt', 'r+') as file:
        for x in file:
            if str(ID) in x:
                s = x.split()[1].split(',')
                name, phone, balance_new = s[0], s[1], int(s[2]) + coins
                old_x, new_x = x, f'{ID} {name},{phone},{balance_new},{datetime.date.today()},0\n'
    with open('UsersInfo.txt', 'r') as file:
        old_data = file.read()
    new_data = old_data.replace(old_x, new_x)
    with open('UsersInfo.txt', 'w') as file:
        file.write(new_data)


def change_data(ID, new_name=None, new_phone=None):
    with open('UsersInfo.txt', 'r+') as file:
        for x in file:
            if str(ID) in x:
                s = x.split()[1].split(',')
                name, phone, balance, date, flag = s[0], s[1], int(s[2]), s[3], s[4]
                if new_phone == None:
                    new_phone = phone
                elif new_name == None:
                    new_name = name
                old_x, new_x = x, f'{ID} {new_name},{new_phone},{balance},{date},{flag}\n'
    with open('UsersInfo.txt', 'r') as file:
        old_data = file.read()
    new_data = old_data.replace(old_x, new_x)
    with open('UsersInfo.txt', 'w') as file:
        file.write(new_data)


def change_flag(ID, flag):
    with open('UsersInfo.txt', 'r+') as file:
        for x in file:
            if str(ID) in x:
                s = x.split()[1].split(',')
                name, phone, balance_new = s[0], s[1], int(x.split()[1].split(',')[2])
                old_x, new_x = x, f'{ID} {name},{phone},{balance_new},{datetime.date.today()},{flag}\n'
    with open('UsersInfo.txt', 'r') as file:
        old_data = file.read()
    new_data = old_data.replace(old_x, new_x)
    with open('UsersInfo.txt', 'w') as file:
        file.write(new_data)


def define_sale_procent(coins):
    if coins < 3000:
        return 1
    if 3000 <= coins < 5000:
        return 0.98
    if 5000 <= coins < 7000:
        return 0.97
    if coins >= 7000:
        return 0.95


def define_date(date):
    months = ['', 'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября',
              'Ноября',
              'Декабря']
    dt = date.split('-')
    return f'{int(dt[2])} {months[int(dt[1])]}'


def define_left_for_sale(coins):
    if coins < 3000:
        return f'До скидки 2% осталось накопить <b>{3000 - coins}</b>'
    if 3000 <= coins < 5000:
        return f'До скидки 3% осталось накопить <b>{5000 - coins}</b>'
    if 5000 <= coins < 7000:
        return f'До скидки 5% осталось накопить <b>{7000 - coins}</b>'
    if coins >= 7000:
        return f'Ты наш постоянный клиент. Наслождайся максимальной <b>5% скидкой</b>!'
