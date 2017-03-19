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
	SHEDULE_MESSAGE = jinja2.Template("{% for event in shedule %}{{event.time}}\n\t\t{{event.title}}\n\n{% endfor %}")
	cur_date = time.strftime("%d.%m.%Y")
	shedule = base.get_day_shedule(bot, cur_date)

	if shedule: reply_message = SHEDULE_MESSAGE.render(shedule=shedule)
	else: reply_message = "Ничего нет"

	bot.telegram.send_message(message.u_id, reply_message, parse_mode="Markdown")
