# Generated by Django 3.1.5 on 2021-04-25 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]