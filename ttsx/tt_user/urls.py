from django.conf.urls import url

from . import views

urlpatterns=[
    url('^register/$',views.register),
    url('^register_handle/$',views.register_handle),
    url('^login/$',views.login),
    # url('^$',views.index),
    url('^register_username/$',views.register_username),
    url('^login_handle/$',views.login_handle),
    url('^register_valid/$',views.register_valid),
    url('^order/$',views.order),
    url('^site/$',views.site),
    url('^islogin/$',views.islogin),
    url('^$',views.center),
    url('^logout/$',views.logout),
]