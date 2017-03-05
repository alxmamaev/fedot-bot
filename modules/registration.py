import telebot
import random
import json


def init(bot):
	bot.handlers["reg-start"] = start
	bot.handlers["reg-get-name"] = get_name
	bot.handlers["reg-get-sex"]	= get_sex
	bot.handlers["reg-get-age"] = get_age
	bot.handlers["reg-get-quad"] = get_quad

def start(bot, message):
	GET_NAME_MESSAGE = random.choice(bot.const["registration-get-name"])
	bot.telegram.send_message(message.u_id, 
							GET_NAME_MESSAGE, 
							reply_markup=telebot.types.ReplyKeyboardRemove(), 
							parse_mode = "Markdown")
	
	bot.user_set(message.u_id, "next_handler", "reg-get-name")

def get_name(bot, message):
	#constants
	GET_SEX_MESSAGE = random.choice(bot.const["registration-get-sex"])
	SEX_KEYBOARD = bot.get_keyboard(bot.const["sex-keyboard"])

	user_name = message.text

	#validation
	if len(user_name.split())!=2:
		start(bot, message)
		return

	#save to redis
	user_info = {
		"id": message.u_id,
		"username": message.from_user.username,
		"name": user_name
	}
	bot.user_set(message.u_id, "info", user_info)

	#ask next question
	bot.telegram.send_message(message.u_id, GET_SEX_MESSAGE, reply_markup = SEX_KEYBOARD)
	bot.user_set(message.u_id, "next_handler", "reg-get-sex")

def get_sex(bot, message):
	#constants
	GET_AGE_MESSAGE = bot.const["registration-get-age"]

	user_sex = bot.get_key(bot.const["sex-keyboard"], message.text)
	
	# validation
	if user_sex is None:
		start(bot, message)
		return
	
	#save to redis
	user_info = bot.user_get(message.u_id, "info")
	user_info["sex"] = user_sex
	bot.user_set(message.u_id, "info", user_info)

	#ask next question
	bot.telegram.send_message(message.u_id, GET_AGE_MESSAGE, reply_markup=telebot.types.ReplyKeyboardRemove())
	bot.user_set(message.u_id, "next_handler", "reg-get-age")

def get_age(bot, message):
	#constants
	GET_QUAD_MESSAGE = bot.const["registration-get-quad"]
	QUADS_KEYBOARD = bot.get_keyboard(bot.const["quads-keyboard"])

	user_age = message.text

	#validation
	if not user_age.isdigit() and 12<int(user_age)<20:
		get_sex(bot, None)
		return

	#save to redis
	user_info = bot.user_get(message.u_id, "info")
	user_info["age"] = user_age
	bot.user_set(message.u_id, "info", user_info)

	#ask next question
	bot.telegram.send_message(message.u_id, GET_QUAD_MESSAGE, reply_markup=QUADS_KEYBOARD)
	bot.user_set(message.u_id, "next_handler", "reg-get-quad")

def get_quad(bot, message):
	user_quad = message.text

	#validation
	if bot.get_key(bot.const["quads-keyboard"], user_quad) is None:
		get_sex(bot, None)
		return

	#save to redis
	user_info = bot.user_get(message.u_id, "info")
	user_info["quad"] = user_quad
	bot.user_delete(message.u_id, "info")

	#register new user
	users = bot.user_get(0, "users") or []
	users.append(user_info)
	bot.user_set(0, "users", users)
	bot.user_set(message.u_id, "register", True)	

	#end of questioning
	bot.telegram.send_message(message.u_id, "Все ок", reply_markup=telebot.types.ReplyKeyboardRemove())
	bot.user_set(message.u_id, "next_handler", "")
	bot.call_handler("main-menu")