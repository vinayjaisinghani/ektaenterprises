from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from core import views as core_views


urlpatterns = [
    #url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^verifymail/$',core_views.verifymail,name="verifymail"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
]