from django.contrib import admin
from .models import Category, Photo, Tag


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ['image', 'title', 'tags']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'style', 'photo_count']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PhotoInline]
    fields = ['name', 'slug', 'style']

    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Кол-во фото'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'tags']
    search_fields = ['title']
    filter_horizontal = ['tags']