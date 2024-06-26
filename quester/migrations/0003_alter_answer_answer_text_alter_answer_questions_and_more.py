# Generated by Django 4.0.4 on 2024-06-17 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quester', '0002_answer_answer_text_question_answer_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=models.CharField(max_length=100, verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='questions',
            field=models.ForeignKey(help_text='Question', on_delete=django.db.models.deletion.CASCADE, to='quester.question'),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='player',
            name='score',
            field=models.IntegerField(default=0, verbose_name='Score'),
        ),
        migrations.AlterField(
            model_name='player',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Subscribe status'),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_count',
            field=models.IntegerField(default=0, verbose_name='Number of correct answers'),
        ),
        migrations.AlterField(
            model_name='question',
            name='comment',
            field=models.CharField(help_text='Comment', max_length=500, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(help_text='Datetime', verbose_name='Datetime'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(help_text='Question text', max_length=1000, verbose_name='Question text'),
        ),
    ]
