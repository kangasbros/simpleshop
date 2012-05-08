from django.conf.urls import patterns, include, url

urlpatterns = patterns('shop.views',
    url(r'^$', include('shop.urls')),
)
