from django.contrib import admin
from .models import Article, UserArticle, ImageArticle

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    def university(self, obj):
        return obj.board.university

    fields = [
        'title',
        'text',
        'is_anonymous',
        'is_question',
        ]
    list_display = [
        'id',
        'university',
        'board',
        'title',
        'text',
        'writer',
        'created_at',
        'is_anonymous',
        'is_question',
        ]

class UserArticleAdmin(admin.ModelAdmin):
    fields = [
        'like',
        'scrap',
        ]
    list_display = [
        'id',
        'user',
        'article',
        'like',
        'scrap',
        ]

class ImageArticleAdmin(admin.ModelAdmin):
    def image_url(self, obj):
        return obj.image.url

    fields = [
        'description',
        ]

    list_display = [
        'id',
        'article',
        'image',
        'description',
        ]

admin.site.register(Article, ArticleAdmin)
admin.site.register(UserArticle, UserArticleAdmin)
admin.site.register(ImageArticle, ImageArticleAdmin)