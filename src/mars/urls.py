from django.conf.urls import include, url
from django.views.generic import TemplateView

from mars import views, forms

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^contact/sent/$', views.sent, name='sent'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about/$', views.about, name='about'),
    url(r'^$', views.home, name='home'),
]
