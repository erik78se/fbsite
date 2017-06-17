from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^tourism/$', views.tourism, name='tourism'),
    url(r'^aker/$', views.aker, name='aker'),
    url(r'^events/register-event/$', views.register_facebook_event, name='register'),

]
