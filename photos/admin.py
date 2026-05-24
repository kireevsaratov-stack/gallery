from django.contrib import admin
from .models import Category, SubCategory, Photo


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'photo_count']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline]

    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Кол-во фото'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'subcategory', 'created_at']
    list_filter = ['category', 'subcategory']
    search_fields = ['title']
