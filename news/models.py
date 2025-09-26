from django.db import models
from django.utils import timezone



class Post(models.Model):
    photo = models.ImageField(
    upload_to='img/news/', verbose_name='Изображение',db_index=True)
    title = models.CharField(max_length=100,verbose_name='Наиминование',)
    content = models.TextField(max_length=1000,verbose_name='Текст',)
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата',)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    
    def __str__(self):
        return self.title