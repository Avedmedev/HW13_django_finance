# Generated by Django 4.1.4 on 2023-01-08 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeapp', '0008_alter_contractor_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='description',
            field=models.CharField(auto_created=True, default='', max_length=150, null=True),
        ),
    ]
