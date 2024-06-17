import telebot
from quester.models import Question, Player, Answer
from chigame.settings import BOT_TOKEN
from datetime import datetime, timedelta
import re

bot = telebot.TeleBot(BOT_TOKEN)

#markup = types.InlineKeyboardMarkup()
#btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://habr.com/ru/all/')
#markup.add(btn1)

DEBUG_BOT = True

@bot.message_handler(commands = ['start'])
def start_func(message):
    player = Player.objects.filter(telegram_id=message.from_user.id)
    if player:
        bot.send_message(message.from_user.id, "Вы уже зарегистрированны")
    else:
        new_player = Player()
        if message.from_user.last_name:
            new_player.name = f"{message.from_user.first_name} {message.from_user.last_name}"
        else:
            new_player.name = f"{message.from_user.first_name}"
        new_player.telegram_id = message.from_user.id
        new_player.status = 1
        new_player.save()
        bot.send_message(message.from_user.id, "Вы зарегистрированны")

@bot.message_handler(regexp = r"^#\d+.+")
def answer_func(message):
    player = Player.objects.get(telegram_id=message.from_user.id)
    question_id = re.findall(r'^#\d+',message.text)
    answer_text = re.sub(r'^#\d+\s+|\s+$','',message.text)
    if question_id:
        question_id = int(re.sub(r'#|\s','',question_id[0]))
    question = Question.objects.filter(id=question_id).first()
    if question:
        bot.send_message(message.from_user.id, question.check_answer(answer_text, player))
    else:
        bot.send_message(message.from_user.id, f"Error. I can't find question №{question_id}")

bot.polling(none_stop=True, interval=0)
