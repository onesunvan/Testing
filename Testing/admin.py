from django.contrib import admin
from Testing import models

# Register your models here.


admin.site.register(models.Subject)
admin.site.register(models.Test)
admin.site.register(models.Question)
admin.site.register(models.Variant)