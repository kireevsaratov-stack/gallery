from django.db import models


class Category(models.Model):
    STYLE_CHOICES = [
        ('wired', 'Wired — ч/б минимализм'),
        ('lovable', 'Lovable — тёплый кремовый'),
        ('clay', 'Clay — яркий игривый'),
        ('raw', 'RAW — авторский'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-имя')
    style = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        default='raw',
        verbose_name='Стиль страницы'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Теги внутри категории: Свадьба, Концерт, Спорт и т.д.
    """
    name = models.CharField(max_length=100, verbose_name='Название тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='Название')
    image = models.ImageField(upload_to='photos/%Y/%m/', verbose_name='Файл')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='photos',
        verbose_name='Теги'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f'Фото {self.id}'