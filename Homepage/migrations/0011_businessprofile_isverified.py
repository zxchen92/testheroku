# Generated by Django 4.1.7 on 2023-04-09 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0010_alter_userprofile_favfood_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessprofile',
            name='isVerified',
            field=models.BooleanField(default=False),
        ),
    ]
