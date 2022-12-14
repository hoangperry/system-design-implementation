# Generated by Django 3.1 on 2022-12-06 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shorten',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('shorten', models.CharField(max_length=7)),
                ('origin', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'shortener',
            },
        ),
    ]
