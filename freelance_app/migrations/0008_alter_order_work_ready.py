# Generated by Django 4.2.5 on 2023-10-03 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_app', '0007_order_work_ready'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='work_ready',
            field=models.CharField(null=True),
        ),
    ]
