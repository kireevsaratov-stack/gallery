from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Category, Photo, Tag


def home(request):
    """Главная страница: список категорий + по 5 последних фото из каждой."""
    categories = Category.objects.prefetch_related('photos').all()

    categories_with_preview = []
    for category in categories:
        preview_photos = category.photos.order_by('-created_at')[:5]
        categories_with_preview.append({
            'category': category,
            'preview_photos': preview_photos,
            'total_count': category.photos.count(),
        })

    return render(request, 'gallery/home.html', {
        'categories_with_preview': categories_with_preview,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    photos = category.photos.order_by('-created_at')

    # Получаем теги только этой категории, убираем None
    tag_filter = request.GET.get('tag')
    tags = category.photos.exclude(tags__isnull=True).values_list('tags__name', flat=True).distinct()
    tags = sorted(set(t for t in tags if t))

    if tag_filter:
        photos = photos.filter(tags__name=tag_filter)

    return render(request, 'gallery/category.html', {
        'category': category,
        'photos': photos,
        'tags': tags,
        'active_tag': tag_filter,
    })


@staff_member_required
def bulk_upload(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)
        files = request.FILES.getlist('images')
        tag_ids = request.POST.getlist('tags')
        new_tags = request.POST.get('new_tags', '').strip()

        # Создаём новые теги из строки через запятую
        created_tags = []
        if new_tags:
            for tag_name in new_tags.split(','):
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    created_tags.append(tag)

        # Объединяем выбранные теги с новыми
        all_tags = list(tag_ids) + [t.id for t in created_tags]

        uploaded_count = 0
        for file in files:
            photo = Photo.objects.create(
                title='',
                image=file,
                category=category,
            )
            if all_tags:
                photo.tags.set(all_tags)
            uploaded_count += 1

        return render(request, 'gallery/upload.html', {
            'categories': Category.objects.all(),
            'tags': Tag.objects.all(),
            'success': f'Загружено {uploaded_count} фото в категорию «{category.name}»',
        })

    return render(request, 'gallery/upload.html', {
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    })