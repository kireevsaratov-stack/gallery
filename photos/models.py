from django.db import models
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-имя')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название подкатегории')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['name']
        unique_together = ['category', 'name']

    def __str__(self):
        return f'{self.category.name} → {self.name}'


class Photo(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='Название')
    image = models.ImageField(upload_to='photos/%Y/%m/', verbose_name='Файл')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        related_name='photos',
        verbose_name='Подкатегория',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f'Фото {self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def resize_image(self):
        if self.image:
            img = Image.open(self.image.path)
            max_size = 1920
            
            if img.width > max_size or img.height > max_size:
                if img.width > img.height:
                    new_width = max_size
                    new_height = int(img.height * (max_size / img.width))
                else:
                    new_height = max_size
                    new_width = int(img.width * (max_size / img.height))
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
                img.save(self.image.path, quality=85, optimize=True)
