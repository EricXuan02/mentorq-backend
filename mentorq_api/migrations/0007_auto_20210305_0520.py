# Generated by Django 3.0.8 on 2021-03-05 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorq_api', '0006_ticket_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
