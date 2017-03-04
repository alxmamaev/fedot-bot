import telebot

def init(bot):
	bot.handlers["reg-start"] = start
	bot.handlers["reg-get-name"] = get_name
	bot.handlers["reg-get-sex"]	= get_sex
	bot.handlers["reg-get-quad"] = get_quad

def start(bot, message):
	GET_NAME_MESSAGE = bot.const["registration-get-name"]
	bot.telegram.send_message(message.u_id, GET_NAME_MESSAGE, reply_markup=telebot.types.ReplyKeyboardRemove())
	
	bot.user_set(message.u_id, "next_handler", "reg-get-name")

def get_name(bot, message):
	GET_SEX_MESSAGE = bot.const["registration-get-sex"]
	SEX_KEYBOARD = bot.get_keyboard(bot.const["sex-keyboard"])

	bot.telegram.send_message(message.u_id, GET_SEX_MESSAGE, reply_markup = SEX_KEYBOARD)
	bot.user_set(message.u_id, "next_handler", "reg-get-sex")

def get_sex(bot, message):
	GET_QUAD_MESSAGE = bot.const["registration-get-quad"]
	QUADS_KEYBOARD = bot.get_keyboard(bot.const["quads-keyboard"])

	if message and bot.get_key(bot.const["sex-keyboard"], message.text) is None:
		start(bot, message)
		return
	
	bot.telegram.send_message(message.u_id, GET_QUAD_MESSAGE, reply_markup=QUADS_KEYBOARD)
	bot.user_set(message.u_id, "next_handler", "reg-get-quad")

def get_quad(bot, message):
	if bot.get_key(bot.const["quads-keyboard"], message.text) is None:
		get_sex(bot, None)
		return

	bot.telegram.send_message(message.u_id, "Все ок", reply_markup=telebot.types.ReplyKeyboardRemove())
	bot.user_set(message.u_id, "next_handler", "")