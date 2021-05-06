from django.db import migrations, models
from django.contrib.postgres.operations import HStoreExtension

class Migration(migrations.Migration):
    dependencies = [
        ('myfinance', '0013_auto_20200801_1757'),
    ]

    operations = [
        HStoreExtension()
    ]