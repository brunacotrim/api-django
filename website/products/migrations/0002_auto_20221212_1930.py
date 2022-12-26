# Generated by Django 3.2 on 2022-12-12 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['id'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=20)),
                ('value', models.CharField(max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='products.product')),
            ],
            options={
                'verbose_name': 'Variation',
                'verbose_name_plural': 'Variations',
                'ordering': ['name', 'value'],
                'unique_together': {('product', 'name', 'value')},
            },
        ),
    ]