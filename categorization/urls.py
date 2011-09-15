from django.conf.urls.defaults import *
 
from categorization.views import *
 
urlpatterns = patterns('', 
  url(
    regex = r'^(?P<slug>[-\w]+)/$',
    view = hierarchy_detail,
    name = 'hierarchy_detail',
    ),
  url(
    regex = r'^(?P<path>[-\w\/]+)/$',
    view = category_detail,
    name = 'category_detail',
    ),
)