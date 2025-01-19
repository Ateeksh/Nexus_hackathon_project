from django.urls import path
from . import views 

urlpatterns = [
    path('block_user', views.block_user, name='block_user'),
    path('Unblocker', views.unblock_user, name='unblock_user'),
]
