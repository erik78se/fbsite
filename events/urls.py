from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register-event/$', views.register_facebook_event, name='Registrera ditt event'),

]
