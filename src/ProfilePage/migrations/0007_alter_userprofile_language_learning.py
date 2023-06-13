# Generated by Django 4.1 on 2023-03-18 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0004_alter_languagemeta_document_path'),
        ('ProfilePage', '0006_alter_userprofile_language_learning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='language_learning',
            field=models.ManyToManyField(blank=True, related_name='learning_profiles', to='HomePage.languagemeta'),
        ),
    ]