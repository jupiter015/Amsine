# Generated by Django 4.1 on 2023-03-31 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CommunityPage', '0003_remove_replies_id_replies_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replies',
            name='uuid',
        ),
        migrations.AddField(
            model_name='replies',
            name='id',
            field=models.BigAutoField(auto_created=True, default=12, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
