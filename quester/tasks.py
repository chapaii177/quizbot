from celery import shared_task
from telegram_bot.bot_active_methods import bot
from quester.models import Player

@shared_task()
def send_question_task(question_id):
    #FIXME add vk bot
    bot.send_question(question_id)

@shared_task()
def send_news_task(news_id):
    #FIXME add vk bot
    bot.send_news(news_id)
