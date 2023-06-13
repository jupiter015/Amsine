# Generated by Django 4.1 on 2023-03-15 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingAuthentication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=8, unique=True)),
                ('email_id', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=15)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('auth_code', models.CharField(editable=False, max_length=5)),
            ],
        ),
    ]
