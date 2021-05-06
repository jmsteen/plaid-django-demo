# Generated by Django 3.0.7 on 2020-08-22 00:22

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myfinance', '0014_hstore_extension'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=200, null=True)),
                ('balances', django.contrib.postgres.fields.hstore.HStoreField()),
                ('mask', models.CharField(max_length=200, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('official_name', models.CharField(max_length=200, null=True)),
                ('subtype', models.CharField(max_length=200, null=True)),
                ('account_type', models.CharField(max_length=200, null=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='orig_descr',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='updated_descr',
        ),
        migrations.AddField(
            model_name='transaction',
            name='account_id',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='account_owner',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='authorized_date',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), null=True, size=None),
        ),
        migrations.AddField(
            model_name='transaction',
            name='category_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='iso_currency_code',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='location',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='merchant_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment_channel',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment_meta',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='pending',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='pending_transaction_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_code',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='unofficial_currency_code',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='AccountNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(max_length=200, null=True)),
                ('account_num_id', models.CharField(max_length=200, null=True)),
                ('routing', models.CharField(max_length=200, null=True)),
                ('wire_routing', models.CharField(max_length=200, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myfinance.Account')),
            ],
        ),
    ]