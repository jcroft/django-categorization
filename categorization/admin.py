from django.contrib import admin
from django.db import models

Category = models.get_model('categorization', 'category')
Hierarchy = models.get_model('categorization', 'hierarchy')

class CategoryAdmin(admin.ModelAdmin):
  list_display        = ('full_name', 'hierarchy', 'path')
  list_filter         = ('hierarchy',)

admin.site.register(Hierarchy)
admin.site.register(Category, CategoryAdmin)