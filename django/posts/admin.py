from django.contrib import admin


from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated', 'created']
    list_display_links = ['updated']
    list_editable = ['title']
    list_filter = ['updated', 'created']

    search_fields = ['title', 'content']

    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
