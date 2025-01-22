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
    path('exersise', views.exercise_info, name='exersise'),
    path('sleep', views.sleep, name='sleep'),
    path('steps', views.steps, name='steps'),
    path('weight', views.weight, name='weight'),
    path('home', views.main, name='home'),
    path('block_user', views.block_user, name='block_user'),
    path('check_name', views.check_name, name='check_name'),
    path('compare_name_pass', views.compare_name_pass, name='compare_name_pass'),
    path('add_account', views.add_account, name='add_account'),
    path('uservalls', views.get_user, name='get_user'),
    path('allvalls/', views.get_all, name='getall'),
    path('set_all_goals', views.set_all_goals, name='set_all_goals'),
    path('get_all_goals', views.get_all_goals, name='get_all_goals'),
    path('set_all', views.set_all, name='set_all'),
]

