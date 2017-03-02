# -*- coding:utf-8 -*-?
import telebot

MENU_MESSAGE = "Чем могу помочь? 😺"
MENU = [[("🏆 Ачивки", "achv-start"), ("📅 Расписание", "sdhl-start")],
        [("🗯 Знакомства", "product-start"), ("👥 Справочник", "test")],
        [("❓ Квест", "product-start"), ("⚙️ Настройки", "test")]]

def init(bot):
    bot.handlers["main-menu"] = menu

def menu(bot, message):
	key = bot.get_key(MENU, message.text)
	if key is not None:
		bot.call_handler(key, message)
		return

	bot.telegram.send_message(message.u_id, MENU_MESSAGE, reply_markup=bot.get_keyboard(MENU))