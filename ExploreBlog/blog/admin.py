from django.contrib import admin
from .models import Post, EditRequest

admin.site.register(Post)
admin.site.register(EditRequest)