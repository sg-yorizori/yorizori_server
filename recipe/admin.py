from django.contrib import admin
from .models import *

admin.site.register(Recipe)
admin.site.register(Ingredients)
admin.site.register(Unit)
admin.site.register(Steps)
