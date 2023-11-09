from django.contrib import admin

from blog.models import Post
from django.db import models
from django.forms import widgets
# Register your models here.

admin.site.register(Post)
