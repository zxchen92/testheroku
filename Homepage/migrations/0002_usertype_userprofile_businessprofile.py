# Generated by Django 4.1.7 on 2023-03-16 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userType', models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('business', 'Business')], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('phone', models.CharField(max_length=8)),
                ('favFood', models.CharField(max_length=30)),
                ('prefLocation', models.CharField(max_length=30)),
                ('foodCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_food_category', to='Homepage.foodcategory')),
                ('userId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=50)),
                ('uen', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=8)),
                ('address', models.CharField(max_length=100)),
                ('postalCode', models.CharField(max_length=6)),
                ('foodCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_food_category', to='Homepage.foodcategory')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
