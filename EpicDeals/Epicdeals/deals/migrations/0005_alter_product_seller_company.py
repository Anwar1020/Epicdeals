# Generated by Django 4.2.1 on 2023-06-10 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0004_seller_company_product_seller_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='seller_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deals.seller_company'),
        ),
    ]