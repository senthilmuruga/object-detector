# Generated by Django 3.1.7 on 2021-03-23 04:17

import detector.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detector', '0003_auto_20210323_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='videos\\%Y\\%m\\%d', validators=[detector.validator.file_size]),
        ),
    ]