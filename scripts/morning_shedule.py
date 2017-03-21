import redis
import json 
import time
import os
import telebot
import jinja2

rds = redis.from_url(os.environ.get("REDIS_URL","redis://localhost:6379"))
key = "user:0:users"
bot = telebot.TeleBot(os.environ.get("BOT_TOKEN",""))

users = rds.get(key)
if type(users) is bytes: users = users.decode('utf-8')
if users: users = json.loads(users)
users = users or []


SHEDULE_MESSAGE = jinja2.Template("*Расписание на сегодня*  📆 \n\n{% for event in shedule %}*{{event.time}}*\n\t{% if event.type == 1 %}☑️ _{% elif event.type>1%}✅* {% else %}◻️ {% endif %}{{event.title}}{% if event.type == 1 %}_{% elif event.type>1%}*{% endif %}\n\n{% endfor %}")
cur_date = time.strftime("%d.%m.%Y")
shedule = base.get_day_shedule(bot, cur_date)

if shedule: reply_message = SHEDULE_MESSAGE.render(shedule=shedule)
else: reply_message = bot.const["shedule-is-empty"]

for user in users:
	bot.send_message(message.u_id, user["id"], parse_mode="Markdown")
