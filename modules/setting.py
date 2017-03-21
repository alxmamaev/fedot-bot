def init(bot):
	bot.handlers["settings-start"] = start
	bot.handlers["settings-get-name"] = get_name
	bot.handlers["settings-get-age"] = get_age
	bot.handlers["settings-get-place"] = get_place
	bot.handlers["settings-get-quad"] = get_quad
	bot.handlers["settings-get-sex"] = get_sex

	bot.handlers["settings-set-name"] = set_name
	bot.handlers["settings-set-age"] = set_age
	bot.handlers["settings-set-place"] = set_place
	bot.handlers["settings-set-quad"] = set_quad
	bot.handlers["settings-set-sex"] = set_sex


def start(bot, message):
	SETTINGS_KEYBOARD = bot.get_keyboard(bot.const["settings-keyboard"])
	SETTINGS_MESSAGE = bot.const["settings-message"]

	key = bot.get_key(bot.const["settings-keyboard"], message.text)

	bot.user_set(message.u_id, "next_handler", "settings-start")

	if not key:
		bot.telegram.send_message(message.u_id, SETTINGS_MESSAGE, reply_markup = SETTINGS_KEYBOARD)
		return

	bot.call_handler(key, message)

def get_name(bot, message):
	GET_NAME_MESSAGE = "Введите ваше имя и фамилию."
	CANCEL_KEYBOARD = bot.get_keyboard(bot.const["cancel-keyboard"])

	bot.telegram.send_message(message.u_id, GET_NAME_MESSAGE, reply_markup = CANCEL_KEYBOARD)
	bot.user_set(message.u_id, "next_handler", "settings-set-name")

def set_name(bot, message): 
	user_name = message.text

	if bot.get_key(bot.const["cancel-keyboard"], message.text) == "cancel": 
		bot.call_handler("settings-start", message)
		return

	#validation
	if len(user_name.split())!=2:
		message.is_forward = True
		bot.call_handler("settings-get-name", message)
		return

	users = bot.user_get(0, "users")
	for i, user in enumerate(users):
		if user["id"] == message.u_id:
			user["name"] = user_name
			users[i] = user

	bot.user_set(0, "users", users)
	bot.call_handler("settings-start", message)
 
def get_age(bot, message):
	GET_AGE_MESSAGE = "Введите ваш возраст."
	CANCEL_KEYBOARD = bot.get_keyboard(bot.const["cancel-keyboard"])

	bot.telegram.send_message(message.u_id, GET_AGE_MESSAGE, reply_markup = CANCEL_KEYBOARD)
	bot.user_set(message.u_id, "next_handler", "settings-set-age")

def set_age(bot, message):
	user_age = message.text

	if bot.get_key(bot.const["cancel-keyboard"], message.text) == "cancel": 
		bot.call_handler("settings-start", message)
		return

	#validation
	if not user_age.isdigit():
		message.is_forward = True
		bot.call_handler("settings-get-age", message)
		return

	users = bot.user_get(0, "users")
	for i, user in enumerate(users):
		if user["id"] == message.u_id:
			user["age"] = int(user_age)
			users[i] = user

	bot.user_set(0, "users", users)
	bot.call_handler("settings-start", message)


def get_place(bot, message):
	GET_AGE_MESSAGE = "Введите ваше место жительства"
	CANCEL_KEYBOARD = bot.get_keyboard(bot.const["cancel-keyboard"])

	bot.telegram.send_message(message.u_id, GET_AGE_MESSAGE, reply_markup = CANCEL_KEYBOARD)
	bot.user_set(message.u_id, "next_handler", "settings-set-place")

def set_place(bot, message):
	user_place = message.text

	if bot.get_key(bot.const["cancel-keyboard"], message.text) == "cancel": 
		bot.call_handler("settings-start", message)
		return

	users = bot.user_get(0, "users")
	for i, user in enumerate(users):
		if user["id"] == message.u_id:
			user["place"] = user_place
			users[i] = user

	bot.user_set(0, "users", users)
	bot.call_handler("settings-start", message)

def get_quad(bot, message):
	GET_AGE_MESSAGE = "Введите ваш отряд."
	QUADS_KEYBOARD = bot.get_keyboard(bot.const["quads-keyboard"])

	bot.telegram.send_message(message.u_id, GET_AGE_MESSAGE, reply_markup = QUADS_KEYBOARD)
	bot.user_set(message.u_id, "next_handler", "settings-set-quad")

def set_quad(bot, message):
	user_quad = bot.get_key(bot.const["quads-keyboard"], message.text)

	if user_quad == "cancel": 
		bot.call_handler("settings-start", message)
		return

	if not user_quad: 
		bot.call_handler("settings-get-quad", message)
		return

	users = bot.user_get(0, "users")
	for i, user in enumerate(users):
		if user["id"] == message.u_id:
			user["quad"] = user_quad
			users[i] = user

	bot.user_set(0, "users", users)
	bot.call_handler("settings-start", message)

def get_sex(bot, message):
	GET_AGE_MESSAGE = "Выберите ваш пол."
	SEX_KEYBOARD = bot.get_keyboard(bot.const["sex-keyboard"])

	bot.telegram.send_message(message.u_id, GET_AGE_MESSAGE, reply_markup = SEX_KEYBOARD)
	bot.user_set(message.u_id, "next_handler", "settings-set-sex")

def set_sex(bot, message):
	user_sex = bot.get_key(bot.const["sex-keyboard"], message.text)

	if user_sex == "cancel": 
		bot.call_handler("settings-start", message)
		return

	if user_sex is None: 
		bot.call_handler("settings-get-sex", message)
		return

	users = bot.user_get(0, "users")
	for i, user in enumerate(users):
		if user["id"] == message.u_id:
			user["sex"] = user_sex
			users[i] = user

	bot.user_set(0, "users", users)
	bot.call_handler("settings-start", message)