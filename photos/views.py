from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Category, SubCategory, Photo


def home(request):
    categories = Category.objects.prefetch_related('photos').all()
    
    categories_with_preview = []
    for category in categories:
        preview_photos = category.photos.order_by('-created_at')[:5]
        categories_with_preview.append({
            'category': category,
            'preview_photos': preview_photos,
            'total_count': category.photos.count(),
        })
    
    return render(request, 'photos/home.html', {
        'categories_with_preview': categories_with_preview,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    # Собираем подкатегории с фото
    subcategories = category.subcategories.prefetch_related('photos').all()
    subcats_with_photos = []
    
    for subcat in subcategories:
        photos = subcat.photos.order_by('-created_at')
        if photos.exists():
            subcats_with_photos.append({
                'name': subcat.name,
                'photos': photos,
            })
    
    # Фото без подкатегории
    untagged_photos = category.photos.filter(subcategory__isnull=True).order_by('-created_at')
    
    return render(request, 'photos/category.html', {
        'category': category,
        'subcats_with_photos': subcats_with_photos,
        'untagged_photos': untagged_photos,
    })


@staff_member_required
def bulk_upload(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)
        subcategory_id = request.POST.get('subcategory')
        subcategory = None
        if subcategory_id:
            subcategory = get_object_or_404(SubCategory, id=subcategory_id)
        
        files = request.FILES.getlist('images')
        
        uploaded_count = 0
        for file in files:
            Photo.objects.create(
                title='',
                image=file,
                category=category,
                subcategory=subcategory,
            )
            uploaded_count += 1
        
        return render(request, 'photos/upload.html', {
            'categories': Category.objects.all(),
            'success': f'Загружено {uploaded_count} фото в «{category.name}»',
        })
    
    return render(request, 'photos/upload.html', {
        'categories': Category.objects.all(),
    })
