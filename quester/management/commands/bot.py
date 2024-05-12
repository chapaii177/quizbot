from django.core.management.base import BaseCommand, CommandError
from telegram_bot.telegram_bot import send_question

class Command(BaseCommand):
    help = "Команды для управления ботом"

    def add_arguments(self, parser):
        parser.add_argument("start")

    def handle(self, *args, **options):
        print(args)
        from telegram_bot import telegram_bot
