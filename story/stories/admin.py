from django.contrib import admin

# Register your models here.
from .models import Story, StoryLike


class StoryLikeAdmin(admin.TabularInline):
    model = StoryLike

class StoryAdmin(admin.ModelAdmin):
    inlines = [StoryLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    class Meta:
        model = Story

admin.site.register(Story, StoryAdmin)


