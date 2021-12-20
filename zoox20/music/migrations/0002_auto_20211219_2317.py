# Generated by Django 3.2.9 on 2021-12-19 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='song',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='music.songs'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='authentication.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
