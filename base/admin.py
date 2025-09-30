from django.contrib import admin
from .models import User, Registration

admin.site.register(User)
admin.site.register(Registration)
# admin.site.index_template = 'custom-admin.html'