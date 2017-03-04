SEX_KEYBOARD = [[("Мальчик 👨‍💻", True), ("Девочка 👩‍💻", False)],[("Меню 🏠", "menu")]]

def init(bot):
	bot.handlers["reg-start"] = start
	bot.handlers["reg-get-name"] = get_name,
	bot.handlers["reg-get-sex"]	= get_sex,
	bot.handlers["reg-get-quad"] = get_quad

def start(bot, message):
	GET_NAME_MESSAGE = bot.const["registration-get-name"]
	bot.telegram.send_message(message.u_id, GET_NAME_MESSAGE)
	bot.user_set(message.u_id, "next_handler", "reg-get-name")

def get_name(bot, message):
	GET_SEX_MESSAGE = bot.const["registration-get-sex"]
	keyboard = bot.get_keyboard(SEX_KEYBOARD)

	bot.telegram.send_message(message.u_id, GET_SEX_MESSAGE, reply_markup = keyboard)
	bot.user_set(message.u_id, "next_handler", "reg-get-sex")

def get_sex(bot, message):
	GET_QUAD_MESSAGE = bot.const["reg-get-quad"]
	bot.telegram.send_message(message.u_id, GET_QUAD_MESSAGE)

def get_quad(bot, message):
	bot.telegram.send_message(message.u_id, "Все ок")
