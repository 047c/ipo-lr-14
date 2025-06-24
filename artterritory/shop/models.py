from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.name}"


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.name} ({self.country})"


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(
        upload_to='products/',
        verbose_name="Фото товара"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Цена"
    )
    quantity = models.IntegerField(
        verbose_name="Количество на складе",
        default=0
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Производитель"
    )

    def __str__(self):
        return f"{self.name} - {self.price}₽"

    def clean(self):
        if self.price < 0:
            raise ValidationError({"price": "Цена не может быть отрицательной"})

        if self.quantity < 0:
            raise ValidationError({"quantity": "Количество не может быть отрицательным"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Trash(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def total_cost(self):
        return sum(item.cost() for item in self.items.all())


class TrashElement(models.Model):
    trash = models.ForeignKey(
        Trash,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0),
                name="quantity_positive"
            )
        ]

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    def cost(self):
        return self.product.price * self.quantity

    def clean(self):
        if self.quantity > self.product.quantity:
            raise ValidationError(
                f"Недостаточно товара на складе. Доступно: {self.product.quantity}"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)