from django.contrib import admin
from .models import User, Post, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
    )  # show username in admin panel userlist despite overriding __str__ in models.py


class PostAdmin(admin.ModelAdmin):
    readonly_fields = (
        "post_time",
        "id",
    )


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
