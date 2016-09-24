from django.contrib import admin
from .models import Post

# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
    list_display= ["title", "published_date", "updated"]
    list_display_links = ["published_date"]
    list_filter = ["title", "updated"]
    search_fields = ["title", "content"]
    list_editable = ["title"]
    fieldsets = [
    (None, {'fields': ['user','title', 'image','content', 'draft',
     'published_date',]
     }),
    ]
    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
