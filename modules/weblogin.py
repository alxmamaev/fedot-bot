import telebot
import random
import os

STANDART_URL = os.environ["WEBHOOK_URL"] + "/login/" 
def init(bot):
	bot.handlers["web-login"] = start

def generate_key(n):
	key = ""
	for i in range(n):
		key += random.choice("qwertyuioopasdfghjklzxcvbnm")
	return key

def start(bot, message):
	key = generate_key(10)
	user_id = message.u_id
	url = STANDART_URL+key

	keys = bot.user_get(0, "login_keys") or {}
	keys[key] = user_id
	print(keys)
	bot.user_set(0, "login_keys", keys)

	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard.add( telebot.types.InlineKeyboardButton("Войти 🔑", url=url))

	bot.telegram.send_message(message.u_id, "Нажмите на кнопку, что бы войти в веб интефейс.", reply_markup = keyboard)