# Generated by Django 3.0.3 on 2020-05-23 08:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('latinoMusic_app', '0008_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processed_payment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
