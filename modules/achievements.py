import random
import telebot
import jinja2


NOT_FOUND_MESSAGES = []
ACHIEVMENTS_LIST_MESSAGE = ""

def init(bot):
	global ACHIEVMENTS_LIST_MESSAGE, NOT_FOUND_MESSAGES

	#Set constants
	NOT_FOUND_MESSAGES = bot.const["achievements-not-found"]
	ACHIEVMENTS_LIST_MESSAGE = jinja2.Template(bot.const["achievements-list"])

	#Set handlers
	bot.handlers["achv-start"] = start

def start(bot, message):
	pass

def give_achievement(bot, message):
	achievements = bot.user_get(message.u_id, "achievements")

	if not achievements: achievements_message = random.choice(NOT_FOUND_MESSAGES)
	else: achievements_message = ACHIEVMENTS_LIST_MESSAGE.render(achievements=achievements.split(";"))

	bot.telegram.send_message(message.u_id, achievements_message)

def give_achievement(bot, u_id, achievement):
	achievements = bot.user_get(message.u_id, "achievements")
	
	if achievements: achievements += ";"+achievement
	else: achievements = achievement

	bot.user_set(u_id, "achievements", achievements)
