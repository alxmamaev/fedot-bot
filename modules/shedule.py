import base
import time
import jinja2

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
	bot.handlers["shed-start"] = start

def start(bot, message):
	SHEDULE_MESSAGE = jinja2.Template(bot.const["shedule-message"])
	cur_date = time.strftime("%d.%m.%Y")
	cur_time = time.localtime()

	shedule = base.get_day_shedule(bot, cur_date)

	flag = False
	for i, event in enumerate(shedule):
		event_time = time.strptime(event["time"], "%H:%M")
		if event_time.tm_hour <= cur_time.tm_hour and event_time.tm_min <= cur_time.tm_min: 
			if not flag: shedule[i]["type"] = 1
			else: shedule[i]["type"] = 2
			flag = True
		else: shedule[i]["type"] = 0

	if shedule: reply_message = SHEDULE_MESSAGE.render(shedule=shedule)
	else: reply_message = bot.const["shedule-is-empty"]

	bot.telegram.send_message(message.u_id, reply_message, parse_mode="Markdown")
