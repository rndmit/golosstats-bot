import os
import subprocess
import threading
import get_stat
import sys
import signal
import re
import time
from logging import log
import telebot


template_popular = "**Самыми популярными словами на сегодня были:** \n"
template_mood = "**Общее настроение авторов:** \n"
template_cash = "**Самые денежные слова на сегодня:** \n"
template_votes = "**Слова, вызывающие наибольшее количество апвойтов:** \n"
template_comms = "**Слова с наибольшим общественным резонансом:** \n"



token = "***" # Токен энивей уже давно не действителен, так что если достанешь из старых коммитов – пользуйся на здоровье
bot = telebot.TeleBot(token)
url = "https://api.telegram.org/bot%s/", token
admins = [275230932, 368898013, 234756807]


@bot.message_handler(commands=['stats'])
def get_stats_msg(message):
    if message.from_user.id in admins:
        bot.send_message(message.chat.id, "Анализирую собранную статистику. Пожалуйста подождите...")

        popular = get_stat.norm_text()
        res_popular = ""

        for item in popular:
            res_popular + item[0] + ": " + str(item[1]) + "\n"

        mood = get_stat.comment_analysis()

        stats = get_stat.hoy(popular, get_stat.get_article_info('2018-02-18'))
        res_cash = ""
        res_votes = ""
        res_comms = ""

        for item in stats:
            res_cash + item["word"] + ": " + item["avg_cash"] + "\n"
            res_votes + item["word"] + ": " + item["avg_votes"] + "\n"
            res_comms + item["word"] + ": " + item["avg_comms"] + "\n"

        bot.send_message(message.chat.id, "Статистика собрана:")
        bot.send_message(message.chat.id, template_popular + res_popular)
        bot.send_message(message.chat.id, template_mood +
                         "Позитивных постов: " + mood["positive_comments"] + "\n" +
                         "Негативных постов: " + mood["negative_comments"] + "\n" +
                         "Нейтральных постов: " + mood["neutral_comments"] + "\n")
        bot.send_message(message.chat.id, template_cash + res_cash)
        bot.send_message(message.chat.id, template_votes + res_votes)
        bot.send_message(message.chat.id, template_comms + res_comms)
    else:
        bot.send_message(message.chat.id, "Простите, но сейчас вы не можете запросить статистику :(")


def main():

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as err:
            time.sleep(30)

def signal_handler(signal_number, frame):
    print('Received signal ' + str(signal_number)
          + '. Trying to end tasks and exit...')
    bot.stop_polling()
    sys.exit(0)

if __name__ == "__main__":
    main()
