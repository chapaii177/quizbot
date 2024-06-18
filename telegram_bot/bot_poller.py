import telebot
from telebot import types
from quester.models import Question, Player, Answer
from chigame.settings import BOT_TOKEN
from datetime import datetime, timedelta
import re


bot = telebot.TeleBot(BOT_TOKEN)

TEXT_COMMANDS = {'change_subscribe':{'quest on': 'Enable subscription to questions',
                                     'quest off': 'Disable subscription to questions',
                                     'news on': 'Enable subscription to news',
                                     'news off': 'Disable subscription to news'},
                 'top': 'Top players',
                 'results': 'Your results',
                 'points': 'Spend points'}

class BotKeyboard(types.ReplyKeyboardMarkup):
    def create_keyboard(self, telegram_id):
        player = Player.objects.get(telegram_id=telegram_id)
        row = []
        row.append(types.KeyboardButton(text=TEXT_COMMANDS['top']))
        row.append(types.KeyboardButton(text=TEXT_COMMANDS['results']))
        row.append(types.KeyboardButton(text=TEXT_COMMANDS['points']))
        self.add(*row, row_width = 3)
        row = []
        if player.status == True:
            text = TEXT_COMMANDS['change_subscribe']['quest off']
        else:
            text = TEXT_COMMANDS['change_subscribe']['quest on']
        row.append(types.KeyboardButton(text))
        if player.status_news == True:
            text = TEXT_COMMANDS['change_subscribe']['news off']
        else:
            text = TEXT_COMMANDS['change_subscribe']['news on']
        row.append(types.KeyboardButton(text))
        self.add(*row, row_width = 2)

@bot.message_handler(commands = ['start'])
def start_func(message):
    player = Player.objects.filter(telegram_id=message.from_user.id)
    if player:
        keyboard = BotKeyboard()
        keyboard.create_keyboard(message.from_user.id)
        bot.send_message(message.from_user.id, "You are already registered", reply_markup=keyboard)
    else:
        new_player = Player()
        if message.from_user.last_name:
            new_player.name = f"{message.from_user.first_name} {message.from_user.last_name}"
        else:
            new_player.name = f"{message.from_user.first_name}"
        new_player.telegram_id = message.from_user.id
        new_player.status = 1
        new_player.save()
        keyboard = BotKeyboard()
        keyboard.create_keyboard(message.from_user.id)
        bot.send_message(message.from_user.id, "Hello", reply_markup=keyboard)

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

@bot.message_handler(func=lambda message: message.text in TEXT_COMMANDS['change_subscribe'].values())
def change_subscribe(message):
    player = Player.objects.get(telegram_id=message.from_user.id)
    if message.text == TEXT_COMMANDS['change_subscribe']['quest on']:
        player.status = True
    elif message.text == TEXT_COMMANDS['change_subscribe']['quest off']:
        player.status = False
    elif message.text == TEXT_COMMANDS['change_subscribe']['news on']:
        player.status_news = True
    elif message.text == TEXT_COMMANDS['change_subscribe']['news off']:
        player.status_news = False
    player.save()
    keyboard = BotKeyboard()
    keyboard.create_keyboard(message.from_user.id)
    bot.send_message(message.from_user.id, "Success", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == TEXT_COMMANDS['top'])
def get_top_players(message):
    players = Player.objects.all().order_by('-score')
    text = 'Top players:'
    i = 1
    for player in players[:10]:
        text += f'\n{i}. {player.__str__()} - {player.score}'
    keyboard = BotKeyboard()
    keyboard.create_keyboard(message.from_user.id)
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == TEXT_COMMANDS['results'])
def get_your_result(message):
    player = Player.objects.get(telegram_id=message.from_user.id)
    keyboard = BotKeyboard()
    keyboard.create_keyboard(message.from_user.id)
    bot.send_message(message.from_user.id, f"Your current points: {player.score}", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == TEXT_COMMANDS['points'])
def spend_ponts(message):
    keyboard = BotKeyboard()
    keyboard.create_keyboard(message.from_user.id)
    bot.send_message(message.from_user.id, "Soon", reply_markup=keyboard)

bot.polling(none_stop=True, interval=0)
