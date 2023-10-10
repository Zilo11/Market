from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(FavoriteItem)
admin.site.register(Review)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id','user','item','rate','created_at']
    readonly_fields = ['created_at']