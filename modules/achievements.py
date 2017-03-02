import telebot

example_message = """*Мои ачивки:*

🥉 _Самый питонист_
🥈 _Не спящий_
🥇 _Быстрый_

*Всего:* 5 ачивок
"""
def init(bot):
	bot.handlers["achv-start"] = start

def start(bot, message):
	bot.telegram.send_message(message.u_id ,example_message, parse_mode="Markdown")
