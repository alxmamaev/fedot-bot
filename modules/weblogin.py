import telebot
import random
import os

STANDART_URL = os.environ["WEBHOOK_URL"] + "/" 
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

	print(4)
	keys = bot.user_get(0, "login_keys") or {}
	keys[key] = user_id
	bot.user_set(0, "login_keys", keys)

	bot.telegram.send_message(message.u_id, url)