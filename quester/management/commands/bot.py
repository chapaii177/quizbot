from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Команды для управления ботом"

    def add_arguments(self, parser):
        parser.add_argument("start")

    def handle(self, *args, **options):
        from telegram_bot import telegram_bot
