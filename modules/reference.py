import random

import telebot
import jinja2


def init(bot):
	bot.handlers["ref-start"] = start
	bot.handlers["ref-get-name"] = get_name

	bot.callback_handlers["ref-next-user"] = next_user


def get_inline_navigation(users, cur_user):
	markup = telebot.types.InlineKeyboardMarkup(row_width=3)
	next_button = telebot.types.InlineKeyboardButton("Далее ⏩",callback_data="ref-next-user/next")
	back_button = telebot.types.InlineKeyboardButton("⏪ Назад",callback_data="ref-next-user/last")

	control_panel = []
	if cur_user != 0: control_panel.append(back_button)
	if cur_user != len(users)-1: control_panel.append(next_button)
	markup.row(*control_panel)

	return markup


def start(bot, message):
	#constants
	GET_USERNAME_MESSAGE = random.choice(bot.const["reference-get-name"])
	BACK_TO_MENU_KEYBOARD = bot.get_keyboard(bot.const["back-to-menu-keyboard"])


	#send start message
	keyboard = BACK_TO_MENU_KEYBOARD
	bot.telegram.send_message(message.u_id, GET_USERNAME_MESSAGE,  reply_markup = keyboard)

	bot.user_set(message.u_id, "next_handler", "ref-get-name")

def next_user(bot, query):
	#constants
	USER_INFO_MESSAGE = jinja2.Template(bot.const["user-info"])

	#read from redis
	users = bot.user_get(query.u_id, "reference_found_users")
	cur_user = bot.user_get(query.u_id, "reference_cur_user")

	#choose next user
	if query.data.split("/")[1] == "next": cur_user+=1
	else: cur_user-=1

	#save to redis
	bot.user_set(query.u_id, "reference_cur_user", cur_user)

	#edit message
	INLINE_NAVIGATION = get_inline_navigation(users, cur_user)
	
	bot.telegram.edit_message_text(chat_id = query.u_id,
							message_id=query.message.message_id, 
							text=USER_INFO_MESSAGE.render(**users[cur_user]),
							reply_markup=INLINE_NAVIGATION,
							parse_mode = "Markdown")	


def get_name(bot, message):
	#constants
	USER_NOT_FOUND_MESSAGE = bot.const["user-not-found"]
	USER_INFO_MESSAGE = jinja2.Template(bot.const["user-info"])
	QUADS = bot.const["quads"]

	#search users
	username = message.text.lower().replace("@", "")
	name = message.text.lower()

	users = bot.user_get(0, "users")
	found_users = []

	for user in users:
		if name in user["name"].lower() or (user["username"] and username in user["username"].lower()): 
			user["quad"] = QUADS.get(user["quad"], "None")
			found_users.append(user)

	
	if not found_users: 
		bot.telegram.send_message(message.u_id, USER_NOT_FOUND_MESSAGE)
		bot.call_handler("ref-get-name", message)
		return

	
	INLINE_NAVIGATION = get_inline_navigation(found_users, 0)

	#save to redis
	bot.user_set(message.u_id, "reference_found_users", found_users)
	bot.user_set(message.u_id, "reference_cur_user", 0)

	#return search result 
	bot.telegram.send_message(message.u_id, 
							USER_INFO_MESSAGE.render(**found_users[0]), 
							reply_markup = INLINE_NAVIGATION,
							parse_mode = "Markdown")

	bot.user_set(message.u_id, "next_handler", "ref-get-name")
