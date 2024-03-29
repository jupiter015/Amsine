# Generated by Django 4.1 on 2023-03-26 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0004_alter_languagemeta_document_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.JSONField()),
                ('languageMeta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='home_user_progresses', to='HomePage.languagemeta')),
                ('userMeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_user_progresses', to='HomePage.usermeta')),
            ],
        ),
    ]
