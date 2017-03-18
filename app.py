# -*- coding:utf-8 -*-?
import os
import sys
import datetime
import base
import flask
import telebot
import logging
from bot import Bot
import random

BOT_TOKEN = os.environ["BOT_TOKEN"]

app = flask.Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route("/bot/<token>", methods=['POST'])
def getMessage(token):
    if token == BOT_TOKEN:
        update = telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))
        bot.proсess_updates(update)
        return "", 200
 
@app.route("/")
def webhook():
    return "Welcome.\n", 200


#SHEDULE
@app.route("/shedule")
def shedule():
    return flask.render_template("shedule.jade", list=[])

@app.route("/shedule/add", methods = ["POST"])
def shedule_add():
    event_id = str(random.randint(10,10000000))
    event_date, event_time, time_type = flask.request.form["date"].split()
    title = flask.request.form["title"]

    base.add(bot, event_id, title, event_date, event_time, time_type)
    return flask.redirect("/shedule")

@app.route("/shedule/edit", methods = ["POST"])
def shedule_edit():
    event_id = flask.request.form["id"]
    event_date, event_time, time_type = flask.request.form["date"].split()
    title = flask.request.form["title"]

    base.delete(bot, event_id)
    base.add(bot, event_id, title, event_date, event_time, time_type)
    return flask.redirect("/shedule")

@app.route("/shedule/delete", methods = ["POST"])
def shedule_delete():
    event_id = flask.request.form["id"]

    base.delete(bot, event_id)
    return flask.redirect("/shedule")


if __name__=="__main__":
    print("Creating bot")
    bot = Bot(debug=False)

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
