# Generated by Django 4.2.5 on 2023-10-02 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_app', '0006_alter_order_deadline_alter_order_degree_to_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='work_ready',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
