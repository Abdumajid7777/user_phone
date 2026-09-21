from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class Accessory(models.Model):
    ACCESSORY_TYPES = (
        ('case', 'Чехол'),
        ('glass', 'Защитное стекло'),
        ('charger', 'Зарядное устройство'),
        ('cable', 'Кабель / Шнур'),
        ('headphones', 'Наушники'),
        ('powerbank', 'Повербанк'),
        ('other', 'Другое'),
    )

    accessory_type = models.CharField(max_length=50, choices=ACCESSORY_TYPES, verbose_name="Тип аксессуара")
    price = models.IntegerField(verbose_name="Цена")
    phone = models.ForeignKey('Phone', on_delete=models.CASCADE, related_name='accessories', verbose_name="Телефон", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    image = models.ImageField(upload_to='accessories/', verbose_name="Изображение", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Аксессуар"
        verbose_name_plural = "Аксессуары"

    def __str__(self):
        return self.accessory_type
    
class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name="Бренд")
    year = models.IntegerField(null=True, blank=True, verbose_name="Год основания") 

    class Meta:
        verbose_name="Бренд"
        verbose_name_plural="Бренды"

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200, verbose_name="Цвет")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name="Цвет"
        verbose_name_plural="Цветы"

class Phone(models.Model):
    CONDITION_CHOICES = (
        ('new', 'Новый'),
        ('used', 'Б/У'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phones', verbose_name='Муаллиф',null=True,blank=True)
    title = models.CharField(max_length=200, verbose_name="Название")
    price = models.IntegerField(verbose_name="Цена ($)")
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, verbose_name="Бренд", null=True, blank=True)
    color = models.ManyToManyField('Color', verbose_name="Цвет")
    image = models.ImageField( verbose_name="Изображение", null=True, blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name="Состояние")
    memory = models.CharField(max_length=50, verbose_name="Память", null=True, blank=True)
    battery = models.IntegerField(verbose_name="Аккумулятор (mAh)", null=True, blank=True)
    internet = models.CharField(max_length=50, verbose_name="Доступ в интернет", null=True, blank=True)
    diagonal = models.FloatField(verbose_name="Диагональ", null=True, blank=True)
    main_camera = models.CharField(max_length=50, verbose_name="Основная камера", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    

    @property
    def average_rating(self):
        reviews = self.reviews.all() 
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0
    
    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"

    def __str__(self):
        return self.title

    pass

class Phone_Parts(models.Model):
    CATEGORY_CHOICES = (
        ('screen', 'Дисплей / Экран'),
        ('battery', 'Аккумулятор'),
        ('camera', 'Камера'),
        ('body', 'Корпус / Задняя крышка'),
        ('charging_port', 'Разъём зарядки'),
        ('motherboard', 'Материнская плата'),
        ('speaker', 'Динамик / Микрофон'),
        ('glass', 'Защитное стекло / Стекло'),
    )

    BRAND_CHOICES = (
        ('apple', 'Apple (iPhone)'),
        ('samsung', 'Samsung'),
        ('xiaomi', 'Xiaomi'),
        ('honor', 'Honor'),
        ('realme', 'Realme'),
        ('huawei', 'Huawei'),
        ('oppo', 'Oppo'),
        ('vivo', 'Vivo'),
        ('google', 'Google Pixel'),
    )

    title = models.CharField(max_length=100, verbose_name='Название запчасти')
    part_type = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Тип запчасти')
    phone_brand = models.CharField(max_length=50, choices=BRAND_CHOICES, verbose_name='Марка телефона')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')

    class Meta:
        verbose_name = 'Запчасть для телефона'
        verbose_name_plural = 'Запчасти для телефонов'

    def __str__(self):
        return self.title

class PhoneReview(models.Model):

    PHONE_RATING = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    )

    phone = models.ForeignKey(
        'Phone',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(verbose_name='Отзыв')
    rating = models.IntegerField(choices=PHONE_RATING, verbose_name='Рейтинг')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв о телефоне'
        verbose_name_plural = 'Отзывы о телефонах'

    def __str__(self):
        return f'{self.phone}'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-id']
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'phone')

    def __str__(self):
        return f"{self.quantity} x {self.phone.title}"
    
    class Meta:
            verbose_name = 'Товар в корзине'
            verbose_name_plural = 'Товары в корзине'
            unique_together = ('cart', 'phone')

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Кутилмоқда'),
        ('processing', 'Ишланмоқда'),
        ('completed', 'Якунланди'),
        ('canceled', 'Бекор қилинди'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.phone.title}"
    
    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, null=True, blank=True, related_name='favorited_by')
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, null=True, blank=True, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['-created_at']
        unique_together = [
            ('user', 'phone'),
            ('user', 'accessory'),
        ]
    def __str__(self):
        item = self.phone if self.phone else self.accessory
        return f"{self.user.username} - {item}"
    

