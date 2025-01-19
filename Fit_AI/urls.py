from django.urls import path
from . import views 

urlpatterns = [
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('assistant', views.Ai, name='login'),
    path('register', views.register, name='login'),
]
