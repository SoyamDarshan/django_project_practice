from django.urls import path, re_path
from . import views

app_name = 'music'

urlpatterns = [
    # /music/
    path('', views.IndexView.as_view(), name='index'),

    # /music/register/
    re_path(r'^register/$', views.UserFormView.as_view(), name='register'),
    # /music/<album_id>/
    re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # music/album/add/
    re_path(r'album/add/$', views.AlbumCreate.as_view(), name='add_album'),

    # music/album/<pk>
    re_path(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='update_album'),

    # music/album/<pk>/delete
    re_path(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='delete_album'),

]