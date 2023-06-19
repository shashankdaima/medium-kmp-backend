from django.urls import path

from . import views

app_name = "ads"

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_new_user, name='register_new_user'),
    path('signin', views.sign_in_user, name='sign_in_user'),
    path('refresh_token', views.refresh_auth_token, name='refresh_auth_token'),
]
