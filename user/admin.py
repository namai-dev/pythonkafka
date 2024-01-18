from django.contrib import admin
from . import models


admin.site.register(models.CustomUser)
admin.site.register(models.UserAccount)
admin.site.register(models.Transaction)
# Register your models here.
