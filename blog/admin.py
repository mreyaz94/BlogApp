from django.contrib import admin
from blog.models import Post,Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'body', 'publish', 'created', 'updated', 'status']
    list_filter = ('status','author' )
    search_fields = ('title','body')
    raw_id_fields = ('author',)  # create id for user at the time of post
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    prepopulated_fields = {'slug':('title',)}  #create slug automatic when inser title

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','body','created','updated','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)



