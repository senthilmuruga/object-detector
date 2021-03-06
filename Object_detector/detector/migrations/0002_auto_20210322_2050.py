# Generated by Django 3.1.7 on 2021-03-22 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('detector', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='source_path',
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_name', models.CharField(max_length=100)),
                ('video', models.FileField(upload_to='videos/')),
                ('date', models.DateField()),
                ('hour', models.CharField(max_length=2)),
                ('camera_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detector.camera')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Detector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=65)),
                ('frame_no', models.IntegerField()),
                ('object_ind', models.CharField(max_length=2083)),
                ('video_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detector.video')),
            ],
        ),
    ]
