# Generated by Django 4.1 on 2023-03-29 20:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('HomePage', '0006_alter_userprogress_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Threads',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('userMeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HomePage.usermeta')),
            ],
        ),
        migrations.CreateModel(
            name='Replies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('parentThread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CommunityPage.threads')),
                ('userMeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HomePage.usermeta')),
            ],
        ),
    ]
