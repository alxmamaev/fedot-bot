import random
import telebot
import jinja2


STANDART_KEYBOARD = [["Меню 🏠", "menu"]]

def init(bot):
	bot.handlers["achv-start"] = start


def start(bot, message):
	if message.u_id in bot.admins: get_username(bot, message)
	else: give_achievement(bot, message)	


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
	bot.telegram.send_message(GET_USERNAME_MESSAGE, reply_markup = keyboard)

	bot.user_set(message.u_id, "next_handler", "achievements-choose-user")

def choose_user(bot, message):
	USER_NOT_FOUND_MESSAGE = bot.const["achievements-user-not-found"]
	USER_INFO_MESSAGE = jinja2.Template(bot.const["achievements-user-info"])

	username = message.text.lower()
	users = json.loads(bot.redis.get("users", "[]"))
	found_users = []

	for user in users:
		if username in user["name"].lower() or username in user["username"].lower(): found_users.append(user_info)


	if not found_users: 
		bot.telegram.send_message(message.u_id, USER_NOT_FOUND_MESSAGE)
		get_username(bot, message)
		return

	bot.user_set(message.u_id, "achievements_found_users", found_users)
	bot.user_set(message.u_id, "achievements_cur_user", 0)

	bot.telegram.send_message(message.u_id, USER_INFO_MESSAGE.render(**found_users[0]))

def next_user(bot, query):
	USER_INFO_MESSAGE = jinja2.Template(bot.const["achievements-user-info"])

	users = bot.user_get(query.u_id, "achievements_found_users")
	cur_user = bot.user_get(query.u_id, "achievements_cur_user")

	if query.data.split("/") == "next": cur_user+=1
	else: cur_user-=1 
	bot.user_set(message.u_id, "achievements_found_users_index", cur_user)

	bot.telegram.edit_message(message=query.message, text=USER_INFO_MESSAGE.render(**users[cur_user]))	

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
	bor.user_set(message.u_id, "next_handler", "achievements-confirm-achievment")

def confirm_achievment(bot, message):
	pass

def give_achievement(bot, message):
	achievements = bot.user_get(message.u_id, "achievements")
	
	if achievements: achievements += ";"+achievement
	else: achievements = achievement

	bot.user_set(message.u_id, "achievements", achievements)

	bot.telegram.send_message("")