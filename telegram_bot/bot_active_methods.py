import telebot
from quester.models import Question, Player, Answer
from chigame.settings import BOT_TOKEN
from datetime import datetime, timedelta
import re

class QuizBot(telebot.TeleBot):
    def send_question(self, question, player):
        players = Player.objects.filter(status = True)
        if players:
            for player in players:
                self.send_message(player.telegram_id, question.text)

bot = QuizBot(BOT_TOKEN)

