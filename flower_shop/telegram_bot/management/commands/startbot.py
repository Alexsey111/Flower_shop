from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Start the Telegram bot'

    def handle(self, *args, **kwargs):
        subprocess.call(['python', 'telegram_bot/bot.py'])
