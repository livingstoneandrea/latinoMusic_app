# Generated by Django 3.0.3 on 2020-05-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('latinoMusic_app', '0003_auto_20200515_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True)),
            ],
        ),
    ]