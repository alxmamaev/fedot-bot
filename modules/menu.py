# -*- coding:utf-8 -*-?
import telebot

def init(bot):
    bot.handlers["main-menu"] = menu

def menu(bot, message):
	MENU_KEYBOARD = bot.get_keyboard(bot.const["menu-keyboard"])
	MENU_MESSAGE = bot.const["menu-message"]

	if message.u_id not in bot.admins and not bot.user_get(message.u_id, "register"):
		bot.call_handler("reg-start", message)
		return

	key = bot.get_key(bot.const["menu-keyboard"], message.text)
	if key is not None:
		bot.call_handler(key, message)
		return

	bot.telegram.send_message(message.u_id, MENU_MESSAGE, reply_markup=MENU_KEYBOARD)