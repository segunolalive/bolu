from django.conf.urls import include, url
from django.contrib import admin

from .views import (
post_list,
post_detail,
post_create,
post_edit,
post_delete,
recent_posts,
month_archive,
year_archive,
)

urlpatterns = [
    url(r'^$', recent_posts, name='recent_posts'),
    url(r'^post/$', post_list, name="list"),
    url(r'^post/create/$', post_create, name="create"),
    url(r'^post/archive/(?P<year>[0-9]{4})/$', year_archive, name="year_archive"),
    url(r'^post/archive/(?P<year>[0-9]{4})/?P<month>([0-9]{2})/$', month_archive, name="month_archive"),
    url(r'^post/(?P<slug>[\w-]+)/$', post_detail, name="detail"),
    url(r'^post/(?P<slug>[\w-]+)/edit/$', post_edit, name="edit"),
    url(r'^post/(?P<slug>[\w-]+)/delete/$', post_delete, name="delete"),

    ]
