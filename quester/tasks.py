from celery import shared_task
from quester.models import Player
from telegram_bot.bot_active_methods import bot

@shared_task()
def send_question(question):
    for player in Player.objects.filter(status=True):
        bot.send_question(question, player)