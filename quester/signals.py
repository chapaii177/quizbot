from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from quester.tasks import send_question_task, send_news_task
#from telegram_bot.bot_active_methods import bot
from quester.models import Question, News
from chigame.celery import app


@receiver(pre_save, sender=Question)
def update_question(sender, instance, **kwargs):
    question = Question.objects.filter(id=instance.id).first()
    if question:
        if question.date != instance.date:
            app.control.revoke(instance.task_id)
            task = send_question_task.apply_async(args=[instance.id],eta=instance.date)
            instance.task_id = task.id

@receiver(post_save, sender=Question)
def create_question(sender, instance, created, **kwargs):
    if created == True:
        task = send_question_task.apply_async(args=[instance.id],eta=instance.date)
        instance.task_id = task.id
        instance.save()

@receiver(post_delete, sender=Question)
def delete_question(sender, instance, **kwargs):
    app.control.revoke(instance.task_id)

@receiver(pre_save, sender=News)
def update_news(sender, instance, **kwargs):
    news = News.objects.filter(id=instance.id).first()
    if news:
        if news.date != instance.date:
            app.control.revoke(instance.task_id)
            task = send_news_task.apply_async(args=[instance.id],eta=instance.date)
            instance.task_id = task.id

@receiver(post_save, sender=News)
def create_news(sender, instance, created, **kwargs):
    if created == True:
        task = send_news_task.apply_async(args=[instance.id],eta=instance.date)
        instance.task_id = task.id
        instance.save()

@receiver(post_delete, sender=News)
def delete_news(sender, instance, **kwargs):
    app.control.revoke(instance.task_id)
