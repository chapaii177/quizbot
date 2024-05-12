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
    question_id = re.findall(r'^#\d+',message.text)
    answer_text = re.sub(r'^#\d+\s+|\s+$','',message.text)
    if question_id:
        question_id = int(re.sub(r'#|\s','',question_id[0]))
    question = Question.objects.filter(id=question_id, )
    if question:
        question = question[0]
        answer = Answer.objects.filter(questions=question,
                                       answer_text__iexact=answer_text)
        if answer:
            player = Player.objects.get(telegram_id=message.from_user.id)
            if player in question.answer_users.all():
                bot.send_message(message.from_user.id, f"Вы уже ответили на вопрос №{question_id}")

            elif question.answer_count < 10:
                player.score += 1
                player.save()
                question.answer_users.add(player)
                question.answer_count += 1
                question.save()
                bot.send_message(message.from_user.id, f"Вы ответили на вопрос №{question_id} в числе первых!!")

            else:
                bot.send_message(message.from_user.id, f"Вы ответили на вопрос №{question_id}, но были игроки быстрее вас")

        else:
            bot.send_message(message.from_user.id, f"Ответ на вопрос №{question_id} неправильный")

    else:
        bot.send_message(message.from_user.id, f"Вопрос №{question_id} уже не активен или не создан")

def send_question():
    questions = Question.objects.filter(date__gte = datetime.now(), date__lte = datetime.now() + timedelta(minutes=20))
    if DEBUG_BOT:
        bot.send_message(140901794, f'Нашлось {len(questions)} вопросов. Время между {datetime.now()} и {datetime.now() + timedelta(minutes=20)}')
    if questions:
        players = Player.objects.filter(status = True)
        if players:
            for player in players:
                bot.send_message(player.telegram_id, question.text)

bot.polling(none_stop=True, interval=0)
