#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import cherrypy
import constant
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


WEBHOOK_HOST = '85.26.164.100'     #'31.130.203.74' #'95.213.236.53'
WEBHOOK_PORT = 443                 # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '85.26.164.100'   #''192.168.43.147'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = 'ssl/webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = 'ssl/webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (constant.token)

bot = telebot.TeleBot(constant.token)


# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)
# -----------------


bot = telebot.TeleBot(constant.token)
print(bot.get_me())

@bot.message_handler(commands=["start"])
def handle_text(message):
    ans = "Добрый день, " + message.from_user.first_name + "! Вас преведствует мистер шляпа"
    from telebot import types
    markup = types.ReplyKeyboardMarkup()
    markup.row('3', '2')
    markup.row('4')
    markup.row('2')
    bot.send_message(message.chat.id, ans, reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global flg
    global k
    chat_id = message.chat.id
    msg = message.text
    bot.send_message(message.chat.id, msg)

# -----------------

# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

 # Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

 # Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})





# Определенный для подключения DNS-суффикс:
# Описание: Беспроводной сетевой адаптер Qualcomm Atheros AR5BWB222
# Физический адрес: ‎E0-06-E6-AA-3B-9F
# DHCP включен: Да
# Адрес IPv4: 192.168.43.147
# Маска подсети IPv4: 255.255.255.0
# Аренда получена: 22 ноября 2018 г. 14:05:59
# Аренда истекает: 22 ноября 2018 г. 17:19:41
# Шлюз по умолчанию IPv4: 192.168.43.1
# DHCP-сервер IPv4: 192.168.43.1
# DNS-серверы IPv4: 194.187.251.67, 185.93.180.131
# WINS-сервер IPv4 :
# Служба NetBIOS через TCP/IP включена: Да
# Локальный IPv6-адрес канала: fe80::7987:6b0c:611d:7232%3
# Шлюз по умолчанию IPv6:
# DNS-сервер IPv6: