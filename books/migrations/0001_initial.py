# Generated by Django 5.0.6 on 2024-06-22 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('borrowing_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('user_reviews', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=50)),
                ('description', models.TextField()),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
    ]
