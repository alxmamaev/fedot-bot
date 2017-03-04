import random
import json
import telebot
import jinja2


STANDART_KEYBOARD = [[("Меню 🏠", "menu")]]

def init(bot):
	bot.handlers["achv-start"] = start
	bot.handlers["achv-choose-user"] = choose_user	

	bot.callback_handlers["achv-news-user"] = next_user
	bot.callback_handlers["achv-news-user"]

def start(bot, message):
	if message.u_id in bot.admins: get_username(bot, message)
	else: get_achievements(bot, message)	


def get_inline_navigation(users, cur_user):
	markup = telebot.types.InlineKeyboardMarkup(row_width=3)
	next_button = telebot.types.InlineKeyboardButton("Далее ⏩",callback_data="achv-news-user/next")
	back_button = telebot.types.InlineKeyboardButton("⏪ Назад",callback_data="achv-news-user/last")
	chouse_user = telebot.types.InlineKeyboardButton("Выбрать ☝🏻", callback_data="achv-choose-user")

	control_panel = []
	if cur_user != 0: control_panel.append(back_button)
	if cur_entrie != entries_count-1: control_panel.append(next_button)
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

	bot.telegram.send_message(message.u_id, achievements_message)



# Give achievement

def get_username(bot, message):
	GET_USERNAME_MESSAGE = bot.const["achievements-get-username"]
	
	keyboard = bot.get_keyboard(STANDART_KEYBOARD)
	bot.telegram.send_message(message.u_id, GET_USERNAME_MESSAGE,  reply_markup = keyboard)

	bot.user_set(message.u_id, "next_handler", "achv-choose-user")

def choose_user(bot, message):
	USER_NOT_FOUND_MESSAGE = bot.const["achievements-user-not-found"]
	USER_INFO_MESSAGE = jinja2.Template(bot.const["achievements-user-info"])

	username = message.text.lower()
	users = json.loads(bot.redis.get("users") or "[]")
	found_users = []

	for user in users:
		if username in user["name"].lower() or username in user["username"].lower(): found_users.append(user_info)


	if not found_users: 
		bot.telegram.send_message(message.u_id, USER_NOT_FOUND_MESSAGE)
		get_username(bot, message)
		return

	bot.user_set(message.u_id, "achievements_found_users", found_users)
	bot.user_set(message.u_id, "achievements_cur_user", 0)


	markup = get_inline_navigation(found_users, 0)
	bot.telegram.send_message(message.u_id, USER_INFO_MESSAGE.render(**found_users[0]), reply_markup)

def next_user(bot, query):
	USER_INFO_MESSAGE = jinja2.Template(bot.const["achievements-user-info"])

	users = bot.user_get(query.u_id, "achievements_found_users")
	cur_user = bot.user_get(query.u_id, "achievements_cur_user")

	if query.data.split("/") == "next": cur_user+=1
	else: cur_user-=1 
	bot.user_set(message.u_id, "achievements_found_users_index", cur_user)

	markup = get_inline_navigation(users, cur_user)
	bot.telegram.edit_message(message=query.message, 
							text=USER_INFO_MESSAGE.render(**users[cur_user]),
							reply_markup=markup)	

def select_user(bot, query):
	USER_INFO_MESSAGE = jinja2.Template(bot.const["achievements-user-info"])
	users = bot.user_get(query.u_id, "achievements_found_users")
	cur_user = bot.user_get(query.u_id, "achievements_cur_user")

	bot.telegram.edit_message(message=query.message, text=USER_INFO_MESSAGE.render(**users[cur_user]))	

	bot.user_set(query.u_id, "achievements_user", users[cur_user])	
	bot.user_delete(query.u_id, "achievements_found_users")
	bot.user_delete(query.u_id, "achievements_cur_user")

	get_achievement_title(bot, query.message)

def get_achievement_title(bot, message):
	GET_ACHIEVMENT_TITLE_MESSAGE = bot.const["achievements-get-title"]

	keyboard = bot.get_keyboard(STANDART_KEYBOARD)
	bot.telegram.send_message(GET_ACHIEVMENT_TITLE_MESSAGE, reply_markup = keyboard)
	bor.user_set(message.u_id, "next_handler", "achv-confirm-achievment")

def give_achievement(bot, message):
	achievements = bot.user_get(message.u_id, "achievements")
	
	if achievements: achievements = [message.text]
	else: achievements.append(message.text)

	bot.user_set(message.u_id, "achievements", achievements)

	bot.telegram.send_message("Готово")