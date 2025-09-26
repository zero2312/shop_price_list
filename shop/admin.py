from django.contrib import admin
from shop import models
from django.utils.safestring import mark_safe
from django_mptt_admin.admin import DjangoMpttAdmin

'''
Модель Category (Категория)
'''
@admin.register(models.Category)
# Настройки Category
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ('title',)
    search_fields = ('title',)

# Настройки Products
class ProductsAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['img_show', 'title', 'price', 'wholesalePrice', 'cost', 'category' ]
    list_editable = ['price', 'wholesalePrice', 'cost']
    list_display_links = ['title']
    ordering = ['category']
    
    """Метод для отображения картинки в Админке"""
    def img_show(self, obj):
        if obj.photo:
            return mark_safe("<img src='{}' width='30' />".format(obj.photo.url))
        return "None"

    img_show.__name__ = "Картинка"
    
# Привязка модели OrderItem к Order
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1

# Настройки  Order
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['name', 'created_at']

#Настройки Контакты  
class ConcactsAdmin(admin.ModelAdmin):
        def has_add_permission(self, request):
        # Получаем количество существующих экземпляров модели Concact
            num_objects = self.model.objects.count()
        # Разрешаем создание нового экземпляра только если их еще нет
            return num_objects == 0
#Регистрация * Нужна для отображения в Админке
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Concacts, ConcactsAdmin)
