from django.urls import path
from . import views 

urlpatterns = [
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('assistant', views.Ai, name='assistant'),
    path('register', views.register, name='register'),
    path('nutrient_counter', views.scan, name='Calors'),
    path('scan/', views.file_upload, name='Nutrient_checker'),
    path('Nutrient_viewer', views.Nutrient_info, name='Calories'),
    path('diet', views.diet, name='diet'),
    path('diets', views.getDiet, name='getdiet'),
    path('excersise', views.Excersise_info, name='excersise'),
    path('sleep', views.sleep, name='sleep'),
    path('steps', views.steps, name='steps'),
    path('weight', views.weight, name='weight'),
    path('home', views.main, name='home'),
    path('block_user', views.block_user, name='block_user'),
    path('user_counter', views.get_user_counter, name='get_user_counter'),
    path('check_name', views.check_name, name='check_name'),
    path('compare_name_pass', views.compare_name_pass, name='compare_name_pass'),
    path('add_account', views.add_account, name='add_account'),
    path('uservalls', views.get_user, name='get_user'),
    path('allvalls/', views.get_all, name='getall'),
]

