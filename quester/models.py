from django.db import models
# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Name")
    telegram_id = models.IntegerField(verbose_name='Telegram id')
    score = models.IntegerField(default=0,
                                verbose_name='Score')
    status = models.BooleanField(default=True,
                                 verbose_name='Subscribe status')

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=1000,
                            verbose_name = 'Question text',
                            help_text='Question text')
    date = models.DateTimeField(verbose_name = 'Datetime',
                            help_text='Datetime')
    comment = models.CharField(max_length=500,
                               verbose_name = "Comment",
                               help_text="Comment")
    answer_count = models.IntegerField(default=0,
                                       verbose_name='Number of correct answers')
    answer_users = models.ManyToManyField(Player, blank=True)

    def __str__(self):
        return self.text[:30] + '...'

    def check_answer(self, answer_text, player):
        answers = Answer.objects.filter(questions=question,
                                        answer_text__iexact=answer_text)
        if answers:
            if player in self.answer_users.all():
               return f"You've already answered the question №{question.id}"
            elif self.answer_count < 10:
                player.score += 1
                player.save()
                self.answer_users.add(player)
                self.answer_count += 1
                self.save()
                return f"The answer to the question №{question.id} is correct!!"
            else:
                return f"he answer to the question №{question.id} is correct, but the other players were faster"
        else:
            return f"The answer to the question №{question.id} is wrong"


class Answer(models.Model):
    questions = models.ForeignKey(Question,
                                  help_text="Question",
                                  on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100,
                                   verbose_name='Answer')

    def __str__(self):
        return self.answer_text


