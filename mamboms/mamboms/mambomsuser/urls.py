from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    (r'^getUserInfo', 'mamboms.mambomsuser.views.get_user_info'),
    (r'^listAllUsers$', 'mamboms.mambomsuser.views.list_all_users'),
    (r'^listUsers$', 'mamboms.mambomsuser.views.list_users'),
    (r'^loadUser$', 'mamboms.mambomsuser.views.load_user'),
    (r'^saveUser$', 'mamboms.mambomsuser.views.save_user'),
    (r'^listAllNodes$', 'mamboms.mambomsuser.views.list_all_nodes'),
    (r'^listNodeUsers$', 'mamboms.mambomsuser.views.list_node_users'),
    (r'^forgotPassword$', 'mamboms.mambomsuser.views.forgot_password'),
    (r'^resetPassword$', 'mamboms.mambomsuser.views.reset_password'),
)
