# Generated by Django 4.2.4 on 2023-09-19 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_management', '0003_alter_quizattempter_quiz_id'),
        ('quiz_attempter_management', '0003_alter_answer_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.IntegerField()),
                ('quiz', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quiz_management.quiz')),
                ('quiz_attempter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quiz_management.quizattempter')),
            ],
        ),
    ]
