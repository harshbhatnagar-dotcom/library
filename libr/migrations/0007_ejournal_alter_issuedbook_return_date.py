# Generated by Django 5.1.7 on 2025-06-05 17:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libr', '0006_issuedbook'),
    ]

    operations = [
        migrations.CreateModel(
            name='EJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('upload', models.FileField(upload_to='ejournals/')),
                ('link', models.URLField(blank=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='return_date',
            field=models.DateField(default=datetime.datetime(2025, 6, 20, 17, 18, 41, 666994, tzinfo=datetime.timezone.utc)),
        ),
    ]
