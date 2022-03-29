# Generated by Django 4.0.3 on 2022-03-29 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='national_id',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='residence',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='phone_number',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]