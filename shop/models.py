from django.db import models
from decimal import Decimal
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User,Group

'''
Модель Products(Продукты, описвает товар в магазине)
'''
class Products(models.Model):
    title = models.CharField(max_length=50, verbose_name='Наиминование', db_index=True)
    photo = models.ImageField(
    upload_to='img/products/', verbose_name='Изображение',db_index=True)
    description = models.TextField(max_length=100, verbose_name='Описание', db_index=True)
    price = models.DecimalField(max_length=6, max_digits=10, decimal_places=2, verbose_name='Цена', db_index=True)
    wholesalePrice = models.DecimalField(max_length=6, max_digits=10, decimal_places=2, verbose_name='Опт.Цена')
    cost = models.CharField(max_length=10, null=True,
                            verbose_name='Количество')
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, verbose_name='Категория', db_index=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

'''
Модель Cart (Карзина)
'''
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        userGrup = Group.objects.all()
        for item in userGrup:
            if item.name == 'VIP':
                return self.product.wholesalePrice* self.quantity
        return self.product.price * self.quantity
            
    
'''
Модель Order (Покупатель)
'''
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20,verbose_name='Телефон')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name= 'Сумма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name= 'Дата создания')
    
    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
    
    def __str__(self):
        return self.name

'''
Модель OrderItem (Заказы)  
'''
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,verbose_name='Пользователь')
    product = models.ForeignKey(Products, on_delete=models.CASCADE,verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1,verbose_name='Количество')
    price = models.DecimalField(max_length=6, max_digits=10, decimal_places=2, verbose_name='Цена')
    wholesalePrice = models.DecimalField(max_length=6, max_digits=10, decimal_places=2, verbose_name='Опт.Цена')
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


'''
Модель Category (Категория)
'''
class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Наиминование',)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Родительская категория')

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

'''
Модель Concacts (Контакты)
'''
class Concacts(models.Model):
    phone = models.CharField(max_length=16, verbose_name='Телефон')
    adress = models.CharField(max_length=30, verbose_name='Адрес')
    telegram = models.CharField(max_length=30, verbose_name='Telegram')

    def __str__(self):
        return self.adress
    
    class Meta:
        verbose_name = 'Котакт'
        verbose_name_plural = 'Контакты'

