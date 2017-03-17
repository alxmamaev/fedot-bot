import string
import random

def init(bot):
	pass

def start(bot, message):
	if not messange.u_id in bot.admins: 
		bot.send(message.u_id, "Введите ключ вашей команды")
		bot.user_set(message.u_id, "next_handler", "quest-get-key")


def get_key(bot, message):
	pass

def get_team_title(bot, message):
	pass

def get_answer(bot, message):
	pass