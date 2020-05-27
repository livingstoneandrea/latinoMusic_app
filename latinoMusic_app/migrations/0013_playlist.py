# Generated by Django 3.0.3 on 2020-05-26 14:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('latinoMusic_app', '0012_testimonial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='latinoMusic_app.Song')),
            ],
        ),
    ]
