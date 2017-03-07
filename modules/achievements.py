import random
import json
import telebot
import jinja2

def init(bot):
	bot.handlers["achv-start"] = start
	bot.handlers["achv-give-achievement"] = give_achievement
	bot.handlers["achv-get-username"] = get_username
	bot.handlers["achv-get-title"] = get_title

	bot.callback_handlers["achv-next-user"] = next_user
	bot.callback_handlers["achv-select-user"] = select_user
	

def start(bot, message):
	if message.u_id in bot.admins: give_achievement(bot, message)
	else: get_achievements(bot, message)	


def get_inline_navigation(users, cur_user):
	markup = telebot.types.InlineKeyboardMarkup(row_width=3)
	next_button = telebot.types.InlineKeyboardButton("Далее ⏩",callback_data="achv-news-user/next")
	back_button = telebot.types.InlineKeyboardButton("⏪ Назад",callback_data="achv-news-user/last")
	chouse_user = telebot.types.InlineKeyboardButton("Выбрать ☝🏻", callback_data="achv-select-user")

	control_panel = []
	if cur_user != 0: control_panel.append(back_button)
	if cur_user != len(users)-1: control_panel.append(next_button)
	markup.row(*control_panel)
	markup.row(chouse_user)

	return markup


# Get acvievements

def get_achievements(bot, message):
	NOT_FOUND_MESSAGES = bot.const["achievements-not-found"]
	ACHIEVMENTS_LIST_MESSAGE = jinja2.Template(bot.const["achievements-list"])
	
	achievements = bot.user_get(message.u_id, "achievements") or []

	if not achievements: achievements_message = random.choice(NOT_FOUND_MESSAGES)
	else: achievements_message = ACHIEVMENTS_LIST_MESSAGE.render(achievements=achievements)

	bot.telegram.send_message(message.u_id, achievements_message, parse_mode = "Markdown") 



# Give achievement

def give_achievement(bot, message):
	#constants
	GET_USERNAME_MESSAGE = bot.const["achievements-get-username"]
	BACK_TO_MENU_KEYBOARD = bot.get_keyboard(bot.const["back-to-menu-keyboard"])


	#send start message
	keyboard = BACK_TO_MENU_KEYBOARD
	bot.telegram.send_message(message.u_id, GET_USERNAME_MESSAGE,  reply_markup = keyboard)

	bot.user_set(message.u_id, "next_handler", "achv-get-username")

def get_username(bot, message):	
	#constants
	USER_NOT_FOUND_MESSAGE = bot.const["achievements-user-not-found"]
	USER_INFO_MESSAGE = jinja2.Template(bot.const["achievements-user-info"])
	QUADS = bot.const["quads"]

	#search users
	username = message.text.lower().replace("@", "")
	name = message.text.lower()

	users = bot.user_get(0, "users")
	found_users = []

	for user in users:
		if name in user["name"].lower() or username in user["username"].lower(): 
			user["quad"] = QUADS.get(user["quad"], "Не определен")
			found_users.append(user)

	
	if not found_users: 
		bot.telegram.send_message(message.u_id, USER_NOT_FOUND_MESSAGE)
		give_achievement(bot, message)
		return

	
	INLINE_NAVIGATION = get_inline_navigation(found_users, 0)

	#save to redis
	bot.user_set(message.u_id, "achievements_found_users", found_users)
	bot.user_set(message.u_id, "achievements_cur_user", 0)


	#return search result 
	bot.telegram.send_message(message.u_id, 
							USER_INFO_MESSAGE.render(**found_users[0]), 
							reply_markup = INLINE_NAVIGATION,
							parse_mode = "Markdown")

	bot.user_set(message.u_id, "next_handler", "achv-get-username")

def next_user(bot, query):
	#constants
	USER_INFO_MESSAGE = jinja2.Template(bot.const["achievements-user-info"])

	#read from redis
	users = bot.user_get(query.u_id, "achievements_found_users")
	cur_user = bot.user_get(query.u_id, "achievements_cur_user")

	#choose next user
	if query.data.split("/") == "next": cur_user+=1
	else: cur_user-=1

	#save to redis
	bot.user_set(query.u_id, "achievements_cur_user", cur_user)

	#edit message
	INLINE_NAVIGATION = get_inline_navigation(users, cur_user)
	
	bot.telegram.edit_message(message_id=query.message, 
							text=USER_INFO_MESSAGE.render(**users[cur_user]),
							reply_markup=INLINE_NAVIGATION)	

def select_user(bot, query):
	#constants
	USER_INFO_MESSAGE = jinja2.Template(bot.const["achievements-user-info"])
	GET_ACHIEVMENT_TITLE_MESSAGE = bot.const["achievements-get-title"]
	BACK_TO_MENU_KEYBOARD = bot.get_keyboard(bot.const["back-to-menu-keyboard"])


	#select user
	users = bot.user_get(query.u_id, "achievements_found_users")
	cur_user = bot.user_get(query.u_id, "achievements_cur_user")
	
	#delete inline keyboard
	bot.telegram.edit_message_text(chat_id=query.u_id,
                                  message_id=query.message.message_id, 
								  text=USER_INFO_MESSAGE.render(**users[cur_user]),
								  parse_mode = "Markdown")	

	#save to redis
	bot.user_set(query.u_id, "achievements_user", users[cur_user])	
	bot.user_delete(query.u_id, "achievements_found_users")
	bot.user_delete(query.u_id, "achievements_cur_user")

	#ask next quesion
	bot.telegram.send_message(query.u_id, GET_ACHIEVMENT_TITLE_MESSAGE, reply_markup = BACK_TO_MENU_KEYBOARD)
	bot.user_set(query.u_id, "next_handler", "achv-get-title")

def get_title(bot, message):
	user = bot.user_get(message.u_id, "achievements_user")	
	achievements = bot.user_get(user["id"], "achievements")
	
	if achievements: achievements.append(message.text)
	else: achievements = [message.text]

	bot.user_set(message.u_id, "achievements", achievements)

	bot.telegram.send_message(message.u_id, "Готово")
	bot.telegram.send_message(user["id"], "У тебя новая ачивка")