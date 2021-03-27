# -*- coding: utf-8 -*-
from telebot import types
import telebot as t
from datetime import datetime
import requests, cfg, json, time, random
bot = t.TeleBot(cfg.token)
#Обращение к API сайта с выводом расписания
def request_for_choose(weekday, weeknum):
    r = requests.get(f'{cfg.domain}/api/?weekday={weekday}&num={weeknum}')
    if r.json()["result"] == True:
        m=r.json()["response"]
        if m!=None:
            t1='✅' if m[1]!= "" else "❌"
            t2='✅' if m[2]!= "" else "❌"
            t3='✅' if m[3]!= "" else "❌"
            t4='✅' if m[4]!= "" else "❌"
            t5='✅' if m[5]!= "" else "❌"
            t6='✅' if m[6]!= "" else "❌"
            text=f"☀{day(weekday)}, неделя №{weeknum}\n\n 🕐Время \t \t 📗Предмет \n {t1}08:30 - 10:00 \t{m[1]}\n {t2}10:15 - 11:45 \t{m[2]}\n {t3}12:00 - 13:30 \t{m[3]}\n {t4}14:00 - 15:30 \t{m[4]}\n {t5}15:45 - 17:15 \t{m[5]}\n {t6}17:30 - 19:00 \t{m[6]}"
        else:
            text='🌚Занятия по расписанию отсутствуют'
    else:
        text="Неизвестная ошибка в запросе❌"
    return text            
def day(a):
    arr=["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресние"]
    for i in range(len(arr)):
        if a == i:
            return arr[i]
def weeknum():
    now = datetime.now()
    #Вывод номера дня недели [0-6]
    week = int(now.strftime("%V"))
    num = 2 if week % 2 == 0 else 1
    return num
@bot.message_handler(commands=['start'])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="📁Меню", callback_data="1")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, f'Расписание группы: ДКЕС_11/1\nДля открытия меню используйте кнопку ниже' , reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        #Окно 2
        if call.data == "1":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            today = types.InlineKeyboardButton(text="☀Расписание на сегодня", callback_data="3")
            choose = types.InlineKeyboardButton(text="🗓Выбрать другой день", callback_data="4")
            full = types.InlineKeyboardButton(text="📜Расписание в PDF Формате", callback_data="2")
            #menu = types.InlineKeyboardButton(text="📁Меню", callback_data="1")
            keyboard.add(today, choose, full)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите:", reply_markup=keyboard)
            #Расписание в pdf
        if call.data == "3":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            menu = types.InlineKeyboardButton(text="📁Меню", callback_data="1")
            keyboard.add(menu)
            nowd = datetime.today()
            j = nowd.weekday()#цифра дня недели
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(j, weeknum()), reply_markup=keyboard)
        #Выбрать другой день        
        if call.data == "4": 
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            menu = types.InlineKeyboardButton(text="📁Меню", callback_data="1")
            a = types.InlineKeyboardButton(text="1⃣", callback_data="101")
            b = types.InlineKeyboardButton(text="2⃣", callback_data="102")
            keyboard.add(a, b, menu)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Выбрите номер недели:", reply_markup=keyboard)
        if call.data == "101" or "102":
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            choose = call.data
            if choose == "101":
                mon = types.InlineKeyboardButton(text="🥱Понедельник", callback_data="1001")
                tues = types.InlineKeyboardButton(text="😮Вторник", callback_data="1002")
                wed = types.InlineKeyboardButton(text="😬Среда", callback_data="1003")
                thur = types.InlineKeyboardButton(text="💪Четверг", callback_data="1004")
                fr = types.InlineKeyboardButton(text="🙃Пятница", callback_data="1005")
                sat = types.InlineKeyboardButton(text="🥂Суббота", callback_data="1006")
                keyboard.add(mon, tues, wed, thur, fr, sat)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Выберите:", reply_markup=keyboard)
              
            elif choose == '102':
                mon = types.InlineKeyboardButton(text="🥱Понедельник", callback_data="1007")
                tues = types.InlineKeyboardButton(text="😮Вторник", callback_data="1008")
                wed = types.InlineKeyboardButton(text="😬Среда", callback_data="1009")
                thur = types.InlineKeyboardButton(text="💪Четверг", callback_data="1010")
                fr = types.InlineKeyboardButton(text="🙃Пятница", callback_data="1011")
                sat = types.InlineKeyboardButton(text="🥂Суббота", callback_data="1012")
                keyboard.add(mon, tues, wed, thur, fr, sat)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Выберите:", reply_markup=keyboard)
       
        if call.data == "1001" or "1002" or "1003" or "1004" or "1005" or "1006":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            menu = types.InlineKeyboardButton(text="📁Меню", callback_data="1")
            c = call.data
            global wd 
            wn=1
            keyboard.add(menu)
            if c == "1001":
                wd=0
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd, wn), reply_markup=keyboard)
            elif c == "1002":
                wd=1
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd, wn), reply_markup=keyboard)
            elif c == "1003":
                wd=2
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd, wn), reply_markup=keyboard)
            elif c == "1004":
                wd=3
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd, wn), reply_markup=keyboard)
            elif c == "1005":
                wd=4
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd, wn), reply_markup=keyboard)
            elif c == "1006":
                wd=5
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd, wn), reply_markup=keyboard)

        if call.data == "1007" or "1008" or "1009" or "1010" or "1011" or "1012":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            menu = types.InlineKeyboardButton(text="📁Меню", callback_data="1")
            c = call.data
            global wd2 
            wn=2
            keyboard.add(menu)
            if c == "1007":
                wd2=0
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd2, wn), reply_markup=keyboard)
            elif c == "1008":
                wd2=1
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd2, wn), reply_markup=keyboard)
            elif c == "1009":
                wd2=2
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd2, wn), reply_markup=keyboard)
            elif c == "1010":
                wd2=3
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd2, wn), reply_markup=keyboard)
            elif c == "1011":
                wd2=4
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd2, wn), reply_markup=keyboard)
            elif c == "1012":
                wd2=5
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=request_for_choose(wd2, wn), reply_markup=keyboard)      
        #pdf расписание
        if call.data == "2":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            link=f'{cfg.domain}/createhtml/file.html'
            r=requests.get(f'{cfg.domain}/createhtml/')
            if r.status_code==200:
                #global get_link
                json={'source': link, 'filename': 'schedule.pdf'}
                n=0
                while n==0:
                    a = random.randint(0, len(cfg.tokens))
                    auth=(cfg.tokens[a], '')
                    try:
                        r1 = requests.post('https://api.pdfshift.io/v3/convert/pdf', auth=auth, json=json)
                        r1.raise_for_status()
                        n=1
                        answer = r1.json()
                        get_link=answer['url']
                        link = types.InlineKeyboardButton(text="Скачать", url=f'{get_link}')
                        menu = types.InlineKeyboardButton(text="📁Меню", callback_data="1")
                        keyboard.add(link, menu)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"📜Расписание в PDF формате:", reply_markup=keyboard)
                    except requests.exceptions.HTTPError:
                        n=0
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Связь с сайтом {cfg.domain} не установлена❌", reply_markup=keyboard)
                menu = types.InlineKeyboardButton(text="📁Меню", callback_data="1")
                keyboard.add(menu)
while True:
    bot.polling(none_stop=True)