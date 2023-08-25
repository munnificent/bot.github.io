import telebot
from telebot import types

bot = telebot.TeleBot('6118471109:AAFBeKishUULGHk3erknaJkKdhD0rfFNeaQ')

products_dict = {
    '1': 'Яблоко',
    '2': 'Молоко',
    '3': 'Хлеб',
    '4': 'Мясо',
    '5': 'Сыр',
    '6': 'Огурец'
}

def webAppKeyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    webAppTest = types.WebAppInfo("https://munnificent.github.io/bot.github.io/")
    one_butt = types.KeyboardButton(text="Тестовая страница", web_app=webAppTest)
    keyboard.add(one_butt)

    return keyboard

@bot.message_handler(content_types="web_app_data")
def answer(webAppMes):
    towar = products_dict[webAppMes.web_app_data.data]

    bot.send_message(webAppMes.chat.id, f"Вы выбрали товар: {towar}")
    send_quantity_keyboard(webAppMes.chat.id, webAppMes.message_id, int(webAppMes.web_app_data.data))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот с одной кнопкой.', reply_markup=webAppKeyboard())

@bot.message_handler()
def handle_message(message):
    if message.text == 'Нажми меня':
        bot.send_message(message.chat.id, 'Кнопка нажата!')

def send_quantity_keyboard(chat_id, message_id_to_delete, product_number, quantity=1):
    bot.delete_message(chat_id, message_id_to_delete)
    towar = products_dict[str(product_number)]
    markup = types.InlineKeyboardMarkup()
    plus_button = types.InlineKeyboardButton(text='+', callback_data=f'plus|{product_number}|{quantity}')
    minus_button = types.InlineKeyboardButton(text='-', callback_data=f'minus|{product_number}|{quantity}')
    confirm_button = types.InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm|{product_number}|{quantity}')
    markup.add(minus_button, plus_button, confirm_button)

    bot.send_message(chat_id, f'Выбран товар {towar}.\nТекущее количество: {quantity}', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    action, product_number, quantity = call.data.split('|')
    product_number = int(product_number)
    quantity = int(quantity)
    towar = products_dict[str(product_number)]

    if action == 'plus':
        quantity += 1
    elif action == 'minus':
        quantity -= 1

    if action == 'confirm':
        bot.answer_callback_query(call.id, f'Вы выбрали товар {towar} в количестве {quantity} шт.')
    else:
        send_quantity_keyboard(call.message.chat.id, call.message.message_id, product_number, quantity)

bot.polling()
