# Generated by Django 3.1.4 on 2021-02-14 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myfinance', '0026_auto_20210213_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='builtin_category',
            field=models.ForeignKey(blank=True, default=260, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myfinance.category'),
        ),
    ]
