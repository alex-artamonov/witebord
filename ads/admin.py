from django.contrib import admin

from .models import Guild, Ad, Reply, Tag


# Register your models here.

class AdsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'updated_at']
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')


admin.site.register(Guild)

admin.site.register(Ad, AdsAdmin)

admin.site.register(Tag)

admin.site.register(Reply)
