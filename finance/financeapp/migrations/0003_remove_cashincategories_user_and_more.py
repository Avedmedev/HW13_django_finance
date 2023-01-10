# Generated by Django 4.1.4 on 2023-01-08 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financeapp', '0002_alter_balance_user_alter_cashincategories_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashincategories',
            name='user',
        ),
        migrations.RemoveField(
            model_name='cashoutcategories',
            name='user',
        ),
        migrations.CreateModel(
            name='UserCashOutCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_out_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financeapp.cashoutcategories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCashInCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_in_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financeapp.cashincategories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='cashin',
            name='cashin_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financeapp.usercashincategories'),
        ),
        migrations.AlterField(
            model_name='cashout',
            name='cashout_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financeapp.usercashoutcategories'),
        ),
    ]