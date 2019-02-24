from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.menu_list, name='menu_list'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'edit/(?P<pk>\d+)/$', views.create_and_edit_menu, name='edit_menu'),
    url(r'create/new/$', views.create_and_edit_menu, name='create_menu'),

]