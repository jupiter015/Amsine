# Generated by Django 4.1 on 2023-03-29 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0006_alter_userprogress_progress'),
        ('CommunityPage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='threads',
            name='languageMeta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HomePage.languagemeta'),
        ),
    ]
