example_message = """*Расписание* на утро 🌝 

08:30 - 09:00 
	☑️ _Завтрак_

09:00 - 10:00 
	☑️ _Соревнование по анализу данных_

10:00 - 11:00 
	✅ *Футбол* 
	▫️> [Подробнее](http://example.com)

11:00 - 12:00
	🎮 Свободное время
	▫️> [Подробнее](http://example.com)
"""

def init(bot):
	bot.handlers["sdhl-start"] = start

def start(bot, message):
	bot.telegram.send_message(message.u_id ,example_message, parse_mode="Markdown")
