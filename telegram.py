import time
import telebot


def token():
    with open("token.txt", "r", encoding="utf-8") as f:
        i = f.readline()
    return i.strip()


API_TOKEN = token()

# Initialize bot and dispatcher
bot = telebot.TeleBot(API_TOKEN)


# Отправка сообщения пользователям бота
def send_message(list_chat_id, text):
    if len(list_chat_id) == 0:
        print('Необходимо написать боту /start')
        return 0

    else:
        for chat_id in list_chat_id:
            bot.send_message(
                chat_id,
                text
            )
        return 1