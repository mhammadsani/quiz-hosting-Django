# Generated by Django 4.2.5 on 2023-09-21 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_management', '0005_remove_quizattempter_quiz_id_quizattempter_quiz_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quizattempter',
            options={},
        ),
        migrations.AlterModelTable(
            name='quizattempter',
            table='Quiz Attempter',
        ),
    ]
