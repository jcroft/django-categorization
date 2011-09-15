from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import get_object_or_404

from categorization.models import *

def category_detail(request, path, template_name='categories/category_detail.html', template_object_name="category", extra_context={}):
  """
  Displays an individual category.
  """
  category = get_object_or_404(Category, path=path)
  return object_detail(
    request,
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra_context,
    object_id = category.id,
    queryset = Category.objects.all(),
  )
  
def hierarchy_detail(request, slug, template_name='categories/hierarchy_detail.html', template_object_name="hierarchy", extra_context={}):
  """
  Displays an individual hierarchy.
  """
  hierarchy = get_object_or_404(Hierarchy, slug=slug)
  return object_detail(
    request,
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra_context,
    object_id = hierarchy.id,
    queryset = Hierarchy.objects.all(),
  )