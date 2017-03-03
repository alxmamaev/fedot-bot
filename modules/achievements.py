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
	
	achievements = bot.user_get(message.u_id, "achievements")

	if not achievements: achievements_message = random.choice(NOT_FOUND_MESSAGES)
	else: achievements_message = ACHIEVMENTS_LIST_MESSAGE.render(achievements=achievements.split(";"))

	bot.telegram.send_message(message.u_id, achievements_message)



# Give achievement

def get_username(bot, message):
	GET_USERNAME_MESSAGE = bot.const["achievements-get-username"]
	
	keyboard = bot.get_keyboard(STANDART_KEYBOARD)
	bot.telegram.send_message(GET_USERNAME_MESSAGE, reply_markup = keyboard)
	bor.user_set(message.u_id, "next_handler", "achievements-choose-user")


def choose_user(bot, message):
	USER_NOT_FOUND_MESSAGE = bot.const["achievements-user-not-found"]

	users = json.loads(bot.redis.get("users", "{}"))
	found_users = []

	if message.text.starts_with("@"): 
		found_users.append(users.get(message.text))
	else:
		for username, user in users.items():
			if message.text.lower() in user_info["name"].lower(): found_users.append(user_info)


	if not found_users: 
		bot.telegram.send_message(message.u_id, USER_NOT_FOUND_MESSAGE)
		bot.user_set(message.u_id, "next_handler", "achievements-get-username")
		return

	bot.user_set(message.u_id, "achievements_found_users", json.dumps(found_users))
	bot.user_set(message.u_id, "achievements_found_users_index", "0")

	bot.user_set(message.u_id, "next_handler", "achievements-get-title")

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