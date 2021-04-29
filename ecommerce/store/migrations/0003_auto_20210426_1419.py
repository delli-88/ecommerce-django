# Generated by Django 3.1.5 on 2021-04-26 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210425_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='completed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='digital',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
