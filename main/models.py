from django.db import models

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