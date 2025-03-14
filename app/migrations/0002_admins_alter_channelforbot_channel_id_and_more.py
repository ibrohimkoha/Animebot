# Generated by Django 5.1.7 on 2025-03-07 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_chat_id', models.BigIntegerField(unique=True)),
            ],
            options={
                'db_table': 'admins',
            },
        ),
        migrations.AlterField(
            model_name='channelforbot',
            name='channel_id',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='channelforforced',
            name='channel_id',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='code',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='serial',
            name='code',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='userbot',
            name='telegram_chat_id',
            field=models.BigIntegerField(unique=True),
        ),
    ]
