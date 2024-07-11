import telebot
from chigame.settings import BOT_TOKEN
from datetime import datetime, timedelta
from quester.models import Question, Player, News
from time import sleep
from telebot.types import InputFile
import re

class QuizBot(telebot.TeleBot):
    def send_question(self, question_id):
        print('start task', datetime.now())
        players = Player.objects.filter(status=True)
        try:
            question = Question.objects.get(id=question_id)
        except:
            #FIXME add delay to task
            print('No instance', f'--{question_id}--')
            sleep(5)
            question = Question.objects.get(id=question_id)
        print('start send', datetime.now())
        for player in players:
            if question.image:
                self.send_photo(player.telegram_id, InputFile(question.image))
            self.send_message(player.telegram_id, f"Question #{question.id}:\n{question.text}\nSend answer like: \n#{question.id} your answer")
        print('end send', datetime.now())

    def send_news(self, news_id):
        print('start task', datetime.now())
        players = Player.objects.filter(status_news=True)
        try:
            news = News.objects.get(id=news_id)
        except:
            #FIXME add delay to task
            print('No instance', f'--{news_id}--')
            sleep(5)
            news = News.objects.get(id=news_id)
        print('start send', datetime.now())
        for player in players:
            if question.image:
                self.send_photo(player.telegram_id, InputFile(question.image))
            self.send_message(player.telegram_id, f"*{news.title}*\n\n{news.text}", parse_mode= 'Markdown')
        print('end send', datetime.now())

bot = QuizBot(BOT_TOKEN)

