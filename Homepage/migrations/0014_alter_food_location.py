# Generated by Django 4.1.7 on 2023-04-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0013_food_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
