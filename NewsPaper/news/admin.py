from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'categoryType', 'dateCreation', 'title', 'text', 'rating')
    list_filter = ('author', 'categoryType', 'rating')
    search_fields = ('title', 'text')

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

