# Generated by Django 4.1 on 2023-03-31 22:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('CommunityPage', '0002_threads_languagemeta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replies',
            name='id',
        ),
        migrations.AddField(
            model_name='replies',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]