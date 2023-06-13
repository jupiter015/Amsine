# Generated by Django 4.1 on 2023-03-18 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0004_alter_languagemeta_document_path'),
        ('ProfilePage', '0007_alter_userprofile_language_learning'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='native_language',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='native_language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='native_profiles', to='HomePage.languagemeta'),
        ),
    ]
