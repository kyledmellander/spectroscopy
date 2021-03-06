from django.conf.urls import include, url
from django.views.generic import TemplateView

from mars import views, forms

urlpatterns = [
    #url(r'^search/$', views.search, name='search'),
    # url(r'^contact/sent/$', views.sent, name='sent'),
    # url(r'^contact/$', views.contact, name='contact'),
    # url(r'^about/$', views.about, name='about'),
    url(r'^meta/$', views.meta, name='meta'),
    url(r'^graph/$', views.graph, name='graph'),
    url(r'^admin/login/$', views.login),
    url(r'^export/$', views.graph, name="export"),
    url(r'^upload/$', views.upload_file, name="upload"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^login/$', views.login),
    url(r'^results/$', views.results, name='home'),
    url(r'^advanced/$', views.advanced, name='advanced'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^ajax/flagSample/$', views.flagSample, name='flagSample'),
    url(r'^$', views.search, name='home'),
]
