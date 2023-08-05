"""URLs module"""
from django.conf.urls import url
from django.urls import include, path, re_path
from social.apps.django_app.views import auth, complete, disconnect

urlpatterns = [
    # authentication / association
    re_path(r'^login/(?P<backend>[^/]+)/$', auth, name='begin'),
    re_path(r'^complete/(?P<backend>[^/]+)/$', complete, name='complete'),
    # disconnection
    re_path(r'^disconnect/(?P<backend>[^/]+)/$', disconnect, name='disconnect'),
    re_path(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$', disconnect, name='disconnect_individual'),
]
