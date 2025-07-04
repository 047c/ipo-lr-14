# Generated by Django 4.2.23 on 2025-06-24 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='warehouse',
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Количество на складе'),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.manufacturer', verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(upload_to='products/', verbose_name='Фото товара'),
        ),
        migrations.CreateModel(
            name='TrashElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
                ('trash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.trash', verbose_name='Корзина')),
            ],
        ),
        migrations.AddConstraint(
            model_name='trashelement',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gt', 0)), name='quantity_positive'),
        ),
    ]
