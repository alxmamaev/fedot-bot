# coding: utf8
import jinja2

def init(bot):
	bot.handlers["warning-start"] = start
	bot.handlers["warning-send"] = send

def start(bot, message):
	START_MESSAGE = bot.const["get-warning"]
	bot.telegram.send_message(message.u_id, START_MESSAGE)

	bot.user_set(message.u_id, "next_handler", "warning-send")

def send(bot, message):
	WARNING_MESSAGE = jinja2.Template(bot.const["warning"]).render(warning = message.text)

	users = bot.user_get(0, "users")

	for user in users:
		bot.telegram.send_message(user["id"], WARNING_MESSAGE, parse_mode = "Markdown")

	bot.telegram.send_message(message.u_id, "Готово", parse_mode = "Markdown")
