# Generated by Django 4.1 on 2023-03-18 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0003_languagemeta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languagemeta',
            name='document_path',
            field=models.FileField(upload_to='HomePage/language_documents/'),
        ),
    ]