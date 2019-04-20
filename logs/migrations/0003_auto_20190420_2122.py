# Generated by Django 2.1.5 on 2019-04-20 21:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import surflogs.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_auto_20190218_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('photo_id', models.AutoField(primary_key=True, serialize=False)),
                ('referencing_id', models.IntegerField(null=True)),
                ('image', models.FileField(default='photos/None/no-img.jpg', storage=surflogs.storage_backends.PrivateMediaStorage(), upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Session_Record',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(default=0)),
                ('session_id', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')),
            ],
        ),
        migrations.CreateModel(
            name='UserSummary',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('photo', models.FileField(default='profile-photos/None/no-img.jpg', upload_to='surflogs-photos')),
            ],
        ),
        migrations.RenameField(
            model_name='session',
            old_name='wave_data_id',
            new_name='wave_data',
        ),
        migrations.RenameField(
            model_name='spot',
            old_name='ideal_wind',
            new_name='ideal_wind_dir',
        ),
        migrations.RemoveField(
            model_name='report',
            name='conditions',
        ),
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.FileField(default='profile-photos/None/no-img.jpg', storage=surflogs.storage_backends.PrivateMediaStorage(), upload_to=''),
        ),
        migrations.AddField(
            model_name='report',
            name='wave_data',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='logs.Wave_Data'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spot',
            name='description',
            field=models.TextField(default=0, max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='report',
            name='notes',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='report',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='time'),
        ),
        migrations.AlterField(
            model_name='session',
            name='notes',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='session',
            name='spot',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='logs.Spot'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='ideal_swell_dir',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='wave_data',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='wave_data',
            name='spot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='logs.Spot'),
        ),
        migrations.AlterField(
            model_name='wave_data',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='time'),
        ),
        migrations.AddField(
            model_name='usersummary',
            name='homespot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logs.Spot'),
        ),
    ]