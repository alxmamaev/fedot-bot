import os
import json
import logging
import importlib

import telebot
import redis


logger = logging.getLogger("fedot-bot")
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO)

class Bot:
    def __init__(self, debug=False):
        self.MENU_BUTTON = "Меню 🏠"

        self.telegram = telebot.TeleBot(os.environ.get("BOT_TOKEN",""))

        self.handlers = {}
        self.debug = debug
        self.callback_handlers = {}
        self.default_handler = "main-menu"

        self.redis = redis.from_url(os.environ.get("REDIS_URL","redis://localhost:6379"))
        self.logger = logger
        self.data = {}


        self.telegram.set_update_listener(self.proсess_updates)

    def collect_modules(self):
        for module_name in os.listdir("modules"):
            if module_name.endswith(".py"):
                module = importlib.import_module("modules.%s"%module_name[:-3])
                module.init(self)

    def user_set(self, user_id, field, value, **kwargs):
        key = "user:%s:%s"%(user_id, field)
        self.redis.set(key, value, kwargs)
        logger.info("user:%s set[%s]>>\"%s\""%(user_id, field, value))

    def user_get(self, user_id, field, default=None):
        key = "user:%s:%s"%(user_id, field)
        value = self.redis.get(key) or default
        if type(value) is bytes:
            value = value.decode('utf-8')
        logger.info("user:%s get[%s]>>\"%s\""%(user_id, field, value))
        return value

    def user_delete(self, user_id, field):
        key = "user:%s:%s"%(user_id, field)
        self.redis.delete(key)
        logger.info("user:%s delete[%s]"%(user_id, field))

    def call_handler(self, handler, message):
        try:
            self.logger.info("user:%s call_handler[%s]"%(message.u_id, handler))
            self.handlers[handler](self, message)
        except Exception as ex:
            self.logger.error(ex)
            if self.debug: raise ex

    def proсess_updates(self, updates):
        if type(updates) is telebot.types.Update:
            if updates.message is not None: self.process_message(updates.message)
            if updates.callback_query is not None: self.process_callback(updates.callback_query)
            return

        for update in updates:
            if type(update) is telebot.types.Message: self.process_message(update)
            if type(update) is telebot.types.CallbackQuery: self.process_callback(update)

    def process_message(self, message):
        message.u_id = message.chat.id
        if message.text == self.MENU_BUTTON: self.user_set(message.u_id, "next_handler", self.default_handler)
        current_handler = self.user_get(message.u_id, "next_handler", default="") or self.default_handler
        self.user_set(message.u_id, "next_handler", self.default_handler)
        try:
            self.logger.info("user:%s call_handler[%s]"%(message.u_id, current_handler))
            self.handlers[current_handler](self, message)
        except Exception as ex:
            self.logger.error(ex)
            if self.debug: raise ex
            self.user_set(message.u_id, "next_handler", self.default_handler)
            self.call_handler(self.default_handler, message)

    def process_callback(self, query):
        query.u_id = query.message.chat.id
        if query.data:
            callback = query.data.split("/")[0]
            try:
                self.logger.info("user:%s callback[%s]"%(query.u_id, query.u_id))
                self.callback_handlers[callback](self, query)
            except Exception as ex:
                self.logger.error(ex)
                if self.debug: raise ex
        else: self.logger.error("user:%s callback[None]"%(query.u_id))


    @staticmethod
    def get_keyboard(keyboard):
        markup = telebot.types.ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
        for row in keyboard:
            keyboard_row = []
            for col in row: keyboard_row.append(telebot.types.KeyboardButton(col[0]))
            markup.row(*keyboard_row)
        return markup

    @staticmethod
    def get_inline_keyboard(keyboard):
        markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        for row in keyboard:
            keyboard_row = []
            for col in row: keyboard_row.append(telebot.types.InlineKeyboardButton(col[0], callback_data=col[1]))
            markup.row(*keyboard_row)
        return markup

    @staticmethod
    def get_key(keyboard, message):
         for row in keyboard:
                for col in row:
                    if message == col[0]: return col[1]
