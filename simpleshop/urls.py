from django.conf.urls import patterns, include, url

urlpatterns = patterns('simpleshop.views',
    url(r'^$', 'index'),
)
