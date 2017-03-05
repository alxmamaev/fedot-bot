# -*- coding:utf-8 -*-?
import os
import sys
import flask
import telebot
import logging
from bot import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]

app = flask.Flask(__name__)

@app.route("/bot/<token>", methods=['POST'])
def getMessage(token):
    if token == BOT_TOKEN:
        update = telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))
        bot.proсess_updates(update)
        return "", 200

@app.route("/")
def webhook():
    return "Welcome.\n", 200

if __name__=="__main__":
    print("Creating bot")
    bot = Bot(debug=True)

    print("Collecting modules")
    bot.collect_modules()

    print("Removing webhook")
    bot.telegram.remove_webhook()
    
    
    if len(sys.argv)>1 and sys.argv[1]=="polling":
        print("Starting bot")
        bot.telegram.polling(none_stop=True)
    else:
        print("Setting webhook")
        WEBHOOK_URL = os.environ["WEBHOOK_URL"]+"/bot/"+os.environ["BOT_TOKEN"]
        bot.telegram.set_webhook(url=WEBHOOK_URL)
    
        print("Starting bot")
        app.run(port=8080)
