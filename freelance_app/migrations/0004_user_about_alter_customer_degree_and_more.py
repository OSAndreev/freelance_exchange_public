# Generated by Django 4.2.5 on 2023-10-01 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_app', '0003_rename_fromwho_dealhistory_from_who_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='degree',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='degree',
            field=models.IntegerField(default=0),
        ),
    ]
