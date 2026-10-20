from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="Пользователь")
    message = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"


# class Coupon(models.Model):
#     code = models.CharField(max_length=50, unique=True, verbose_name="Код купона")
#     discount_percent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="Процент скидки")
#     valid_from = models.DateTimeField(verbose_name="Действует с")
#     valid_to = models.DateTimeField(verbose_name="Действует до")
#     active = models.BooleanField(default=True, verbose_name="Активен")

#     def is_valid(self):
#         now = timezone.now()
#         return self.active and self.valid_from <= now <= self.valid_to

#     class Meta:
#         verbose_name = "Купон"
#         verbose_name_plural = "Купоны"

#     def __str__(self):
#         return self.code

    
class Review(models.Model):
    product = models.ForeignKey('Phone', on_delete=models.CASCADE, related_name='reviews', verbose_name="Телефон")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} балл.)"


class Accessory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='accessories/', verbose_name="Изображение", null=True, blank=True)

    class Meta:
        verbose_name = "Аксессуар"
        verbose_name_plural = "Аксессуары"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название бренда")
    year = models.IntegerField(null=True, blank=True, verbose_name="Год основания") 

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Название цвета")

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return self.name


class Phone(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название телефона", default='')
    description = models.TextField(verbose_name="Описание", default='', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='phones', verbose_name="Бренд", null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='phones', verbose_name="Цвет", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина: {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Корзина")
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, verbose_name="Телефон")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = ('cart', 'phone')

    def __str__(self):
        return f"{self.phone.name} ({self.quantity} шт.)"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Пользователь")
    status = models.CharField(max_length=20, default='pending', verbose_name="Статус")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Общая сумма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, verbose_name="Телефон")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"{self.phone.name} x {self.quantity}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="Пользователь")
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, verbose_name="Телефон")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        unique_together = ('user', 'phone')

    def __str__(self):
        return f"{self.user.username} -> {self.phone.name}"