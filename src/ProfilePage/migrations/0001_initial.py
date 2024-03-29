# Generated by Django 4.1 on 2023-03-18 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('HomePage', '0004_alter_languagemeta_document_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=80)),
                ('interests', models.CharField(choices=[('travelling', 'Travelling'), ('reading', 'Reading'), ('gaming', 'Gaming')], max_length=15)),
                ('language_learning', models.ManyToManyField(related_name='learning_profiles', to='HomePage.languagemeta')),
                ('last_language_used', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_used_profiles', to='HomePage.languagemeta')),
                ('native_language', models.ManyToManyField(related_name='native_profiles', to='HomePage.languagemeta')),
                ('userMeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profiles', to='HomePage.usermeta')),
            ],
        ),
    ]
