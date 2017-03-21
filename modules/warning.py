# coding: utf8
import jinja2
import random

def init(bot):
	bot.handlers["warning-start"] = start
	bot.handlers["warning-send"] = send

def start(bot, message):
	START_MESSAGE = bot.const["get-warning"]
	BACK_TO_MENU_KEYBOARD = bot.get_keyboard(bot.const["back-to-menu-keyboard"])

	bot.telegram.send_message(message.u_id, START_MESSAGE, reply_markup = BACK_TO_MENU_KEYBOARD)

	bot.user_set(message.u_id, "next_handler", "warning-send")

def send(bot, message):
	WARNING_MESSAGE = jinja2.Template(bot.const["warning"]).render(warning = message.text)
	READY_MESSAGE = random.choice(bot.const["ready"])

	users = bot.user_get(0, "users")

	for user in users:
		bot.telegram.send_message(user["id"], WARNING_MESSAGE, parse_mode = "Markdown")

	bot.telegram.send_message(message.u_id, READY_MESSAGE, parse_mode = "Markdown")
	bot.call_handler("main-menu")
