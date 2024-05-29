#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class DefineUser:
    def __init__(self, ID):
        flag = True
        ID = str(ID)
        self.ID = ID
        with open('UsersInfo.txt', 'r+', encoding='utf-8') as file:
            for x in file:
                if ID in x:
                    self.name = x.split()[1].split(',')[0]
                    self.phone = x.split()[1].split(',')[1]
                    self.balance = int(x.split()[1].split(',')[2])
                    self.date = x.split()[1].split(',')[3]
                    self.flag = x.split()[1].split(',')[4]
                    flag = False
                    break
        if flag:
            self.ID = None