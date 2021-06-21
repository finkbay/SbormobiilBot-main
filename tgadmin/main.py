import telebot
from telebot import types
import configg
from sqlite3 import Error
import sqlite3

bot = telebot.TeleBot(configg.token)

user_data = {}


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# Основное меню

@bot.message_handler(commands=['start'])
def any_msg(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)

    timetable_button = types.InlineKeyboardButton(text="Расписание рейсов", callback_data="timetable")
    materials_button = types.InlineKeyboardButton(text="Что мы принимаем", callback_data="materials")
    report_button = types.InlineKeyboardButton(text="Отчёт о собранном", callback_data="report")

    preparation_button = types.InlineKeyboardButton(text="Как подготовить вторс.", callback_data="preparation")
    marking_button = types.InlineKeyboardButton(text="Маркировки", callback_data="marking")
    remain_button = types.InlineKeyboardButton(text="Куда сдать остальное", callback_data="remain")

    user_report_button = types.InlineKeyboardButton(text="Ваш отчёт о сданном", callback_data="user_report")

    keyboardmain.add(timetable_button, materials_button, report_button, preparation_button, marking_button,
                     remain_button, user_report_button)
    bot.send_message(message.chat.id, "Здраствуйте! У меня есть готовые ответы на самые частые вопросы о Сбормобиле."
                                      "", reply_markup=keyboardmain)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(callback):
    # Возвращение к основному меню

    if callback.data == "mainmenu":
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)

        timetable_button = types.InlineKeyboardButton(text="Расписание рейсов", callback_data="timetable")
        materials_button = types.InlineKeyboardButton(text="Что мы принимаем", callback_data="materials")
        report_button = types.InlineKeyboardButton(text="Отчёт о собранном", callback_data="report")

        preparation_button = types.InlineKeyboardButton(text="Как подготовить вторс.", callback_data="preparation")
        marking_button = types.InlineKeyboardButton(text="Маркировки", callback_data="marking")
        remain_button = types.InlineKeyboardButton(text="Куда сдать остальное", callback_data="remain")

        user_report_button = types.InlineKeyboardButton(text="Ваш отчёт о сданном", callback_data="user_report")

        keyboardmain.add(timetable_button, materials_button, report_button, preparation_button, marking_button,
                         remain_button, user_report_button)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text="Что вы хотите узнать?", reply_markup=keyboardmain)

    # Вывод информации о расписании.

    if callback.data == "timetable":

        connection = create_connection(configg.sqlite3_file)

        select_all = "SELECT * from ugc_timetable"
        new_timetable = execute_read_query(connection, select_all)

        bot.send_message(callback.message.chat.id, "Расписание")

        for id, date, street in new_timetable:
            bot.send_message(callback.message.chat.id, f"  {id}, {date}, {street}")

        connection.close()

    # Меню "что мы принимаем"

    elif callback.data == "materials":

        keyboard = types.InlineKeyboardMarkup()

        wastepaper_button = types.InlineKeyboardButton(text="Макулатура", callback_data="wastepaper")
        glass_button = types.InlineKeyboardButton(text="Стеклотара", callback_data="glass")
        plastic_button = types.InlineKeyboardButton(text="Пластик", callback_data="plastic")

        aluminum_button = types.InlineKeyboardButton(text="Алюминиевые банки", callback_data="aluminum")
        metal_button = types.InlineKeyboardButton(text="Металл", callback_data="metal")
        caps_button = types.InlineKeyboardButton(text="Добрые крышечки", callback_data="caps")

        backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")

        keyboard.add(wastepaper_button, glass_button, plastic_button, aluminum_button, metal_button,
                     caps_button, backbutton)

        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text="Информация о принимаемых материалах", reply_markup=keyboard)

    # Вывод информации с остальных кнопок основного меню

    elif callback.data == "preparation":

        bot.answer_callback_query(callback_query_id=callback.id, show_alert=True,
                                  text="Информация о подготовке вторсырья")

    elif callback.data == 'report':

        connection = create_connection(configg.sqlite3_file)

        select_all = "SELECT * from ugc_profile"

        new_report = execute_read_query(connection, select_all)

        bot.send_message(callback.message.chat.id, "Отчёт о собранном")

        for id, name, amount in new_report:
            bot.send_message(callback.message.chat.id, f"  {id}, {name}, {amount}")

        connection.close()

    elif callback.data == "marking":
        bot.answer_callback_query(callback_query_id=callback.id, show_alert=True, text="Что-то о маркировках")

    elif callback.data == "remain":
        bot.answer_callback_query(callback_query_id=callback.id, show_alert=True, text="Какой-то адресс")

    # Вывод информации из меню *что мы принимаем*

    elif callback.data == "wastepaper":
        bot.answer_callback_query(callback_query_id=callback.id, show_alert=True, text="Что-то про макулатуру")

    elif callback.data == "glass":
        bot.answer_callback_query(callback_query_id=callback.id, show_alert=True, text="Что-то про стеклотару")

    elif callback.data == "plastic":
        bot.answer_callback_query(callback_query_id=callback.id, show_alert=True, text="Что-то про пластик")

    elif callback.data == "aluminum":
        bot.answer_callback_query(callback_query_id=callback.id, show_alert=True, text="Что-то про Алюминиевые банки")

    elif callback.data == "metal":
        bot.answer_callback_query(callback_query_id=callback.id, show_alert=True, text="Что-то про Металл")

    elif callback.data == "caps":
        bot.answer_callback_query(callback_query_id=callback.id, show_alert=True, text="Что-то про добрые крышечки")



    elif callback.data == "user_report":

        class User:
            def __init__(self, material):
                self.material = material
                self.amount = ''

        @bot.message_handler(commands=['material'])
        def send_welcome(message):
            msg = bot.send_message(message.chat.id, "Введите название сданного вами материала")
            bot.register_next_step_handler(msg, process_material_step)

        def process_material_step(message):
            try:
                user_id = message.from_user.id
                user_data[user_id] = User(message.text)

                msg = bot.send_message(message.chat.id, "Сколько вы сдали?")
                bot.register_next_step_handler(msg, process_amount_step)
            except Exception as e:
                bot.reply_to(message, 'Ошибка')

        def process_amount_step(message):
            try:
                connection = create_connection(configg.sqlite3_file)
                cursor = connection.cursor()
                user_id = message.from_user.id
                user = user_data[user_id]
                user.amount = message.text

                sqlite_insert = """INSERT INTO ugc_userreport (user_id, material, amount) 
                                          VALUES (?, ?, ?);"""
                data_in = (user_id, user.material, user.amount)
                count = cursor.execute(sqlite_insert,data_in)
                connection.commit()
                print("Запись успешно вставлена в таблицу  ", cursor.rowcount)
                cursor.close()
                bot.send_message(message.chat.id, "Ваш отчёт отправлен!")

            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
            finally:
                if connection:
                    connection.close()
                    print("Соединение с SQLite закрыто")


if __name__ == "__main__":
    bot.polling(none_stop=True)
