# Generated by Django 2.2.7 on 2019-11-18 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('age', models.FloatField(max_length=20)),
                ('weight', models.FloatField(max_length=20)),
                ('height', models.FloatField(max_length=20)),
                ('birthdate', models.DateField()),
            ],
        ),
    ]
