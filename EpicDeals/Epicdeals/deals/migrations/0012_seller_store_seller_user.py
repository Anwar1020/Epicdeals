# Generated by Django 4.2.1 on 2023-06-14 05:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deals', '0011_rename_store_name_seller_store_store_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller_store',
            name='seller_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
