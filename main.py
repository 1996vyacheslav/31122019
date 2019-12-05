import telebot
import random

bot = telebot.TeleBot('980391805:AAE-uDOTgqzGsvIjTGtcbA9U4ZPdMipZGfc')

santa = ""

list_baza = ["Кухарева", "Пряхин", "Рапопорт", "Линник", "Анпилова",
           "Козловская", "Комарова", "Чабан", "Павлинова", "Русанов",
           "Мельникова", "Антонова", "Знобищева"]
dict_assoc = {"Кухарева":[0, 0], "Пряхин":[0, 0], "Рапопорт":[0, 0], "Линник":[0, 0], "Анпилова":[0, 0],
           "Козловская":[0, 0], "Комарова":[0, 0], "Чабан":[0, 0], "Павлинова":[0, 0], "Русанов":[0, 0],
           "Мельникова":[0, 0], "Антонова":[0, 0], "Знобищева":[0, 0]}

list_deja_choisi = []

keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row("Кухарева")
keyboard.row("Пряхин")
keyboard.row("Рапопорт")
keyboard.row("Линник")
keyboard.row("Анпилова")
keyboard.row("Козловская")
keyboard.row("Комарова")
keyboard.row("Чабан")
keyboard.row("Павлинова")
keyboard.row("Русанов")
keyboard.row("Мельникова")
keyboard.row("Антонова")
keyboard.row("Знобищева")

inline_kb1 = telebot.types.InlineKeyboardMarkup()
inline_btn_1 = telebot.types.InlineKeyboardButton(text='Да', callback_data='button1')
inline_btn_2 = telebot.types.InlineKeyboardButton(text='Нет', callback_data='button2')
inline_kb1.add(inline_btn_1, inline_btn_2)


@bot.message_handler(commands=['start'])
def start_message(message):
   bot.send_message(message.chat.id, "Будем же честны друг с другом и не будем подсматривать кто кому дарит из других "
                                     "пользователей, потому что мне было лень писать обработку по вашему id")
   bot.send_message(message.chat.id, 'Привет, как тебя зовут?', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    global santa
    santa = message.text
    bot.send_message(message.chat.id, "Привет, " + santa + ", это точно ты? (Не, ну я серьезно,"
                                                           "иначе весь кайф обламаешь, так что "
                                                           "будь честен)", reply_markup=inline_kb1)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('button'))
def process_callback_kb1btn1(callback_query):
    global santa
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 1:
        lier = 0
        id = callback_query.from_user.id

        for d in dict_assoc:
            tmp = dict_assoc[d][1]
            if tmp == id:
                if santa != d:
                    lier = 1

        if lier == 0:
            if dict_assoc[santa] == [0, 0]:
                p = 0
                while p == 0:
                    goal = random.choice(list_baza)
                    if goal == santa:
                        goal = random.choice(list_baza)
                    else:
                        p = 1

                bot.answer_callback_query(callback_query.id, text='Твоя цель: ' + goal)
                dict_assoc[santa] = [goal, callback_query.from_user.id]
                list_baza.remove(goal)
            else:
                bot.answer_callback_query(callback_query.id, text='Твоя цель: ' + dict_assoc[santa][0])
        else:
            bot.answer_callback_query(callback_query.id, text="Обманщик!")
            bot.send_message(callback_query.message.chat.id, "Ну и кого ты пытаешься обмануть", reply_markup=keyboard)

    if code == 2:
        bot.answer_callback_query(callback_query.id, text="Внимательнее!")
        bot.send_message(callback_query.message.chat.id, "Попробуй еще раз", reply_markup=keyboard)




bot.polling(none_stop=True, interval=0)