from django.contrib import admin
from .models import Post , Account , Comment

# Register your models here.

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title' , 'author' , 'publish' , 'status',)
    list_editable = ('status',)
    prepopulated_fields = {'slug' : ('title',)} #auto fill slug when writing title
    raw_id_fields = ('author',)


@admin.register(Account)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('phone',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name' , 'post' , 'created' , 'active')
    list_filter = ('active' , 'created')
    list_editable = ('active',)
    search_fields = ('name' , 'email' , 'body')
    actions = ['approve_comments']

    def approve_comments(self , request , queryset):
        queryset.update(active = True)