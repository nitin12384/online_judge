# Generated by Django 4.0.5 on 2022-07-09 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_alter_submission_verdict'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='verdict_type',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
