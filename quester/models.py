from django.db import models
# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Имя и фамилия игрок")
    telegram_id = models.IntegerField(verbose_name='Telegram id')
    score = models.IntegerField(default=0,
                                verbose_name='Количество баллов')
    status = models.BooleanField(default=True,
                                 verbose_name='Статус')

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=1000,
                            verbose_name = 'Текст вопроса',
                            help_text='Текст вопроса')
    date = models.DateTimeField(verbose_name = 'Дата отправки вопроса',
                            help_text='Дата отправки вопроса')
    comment = models.CharField(max_length=500,
                               verbose_name = "Комментарий",
                               help_text="Комментарий")
    answer_count = models.IntegerField(default=0,
                                       verbose_name='Количество правильных ответов')
    answer_users = models.ManyToManyField(Player, blank=True)

    def __str__(self):
        return self.text[:30] + '...'

class Answer(models.Model):
    questions = models.ForeignKey(Question,
                                  help_text="Вопрос",
                                  on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100,
                                   verbose_name='Ответ на вопрос')

    def __str__(self):
        return self.answer_text


