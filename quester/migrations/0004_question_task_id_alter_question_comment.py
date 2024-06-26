# Generated by Django 4.0.4 on 2024-06-18 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quester', '0003_alter_answer_answer_text_alter_answer_questions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='task_id',
            field=models.CharField(blank=True, help_text='Celery task id', max_length=500, verbose_name='Celery task id'),
        ),
        migrations.AlterField(
            model_name='question',
            name='comment',
            field=models.CharField(blank=True, help_text='Comment', max_length=500, verbose_name='Comment'),
        ),
    ]
