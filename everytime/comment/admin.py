from django.contrib import admin
from .models import Comment, UserComment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    def parent_id(self, obj):
        return obj.article.id

    def parent_id(self, obj):
        return obj.id

    fields = [
        'text',
        'is_active',
        ]
    list_display = [
        'id',
        'article_id',
        'parent_id',
        'is_subcomment',
        'text',
        'created_at',
        'commenter',
        'is_writer',
        'is_anonymous',
        'is_active',
        ]

class UserCommentAdmin(admin.ModelAdmin):
    fields = [
        'like',
        'scrap',
        ]
    list_display = [
        'id',
        'user',
        'comment',
        'like',
        ]

admin.site.register(Comment, CommentAdmin)
admin.site.register(UserComment, UserCommentAdmin)