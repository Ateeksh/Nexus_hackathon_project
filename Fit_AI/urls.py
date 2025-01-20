from django.urls import path
from . import views 

urlpatterns = [
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('assistant', views.Ai, name='assistant'),
    path('register', views.register, name='register'),
    path('nutrient_counter', views.scan, name='Calories'),
    path('scan/', views.file_upload, name='Nutrient_checker'),
    path('Nutrient_viewer', views.Nutrient_info, name='Calories'),
    path('diet', views.diet, name='diet-viewer'),
    path('excersise', views.Excersise_info, name='diet-viewer'),
    path('sleep', views.sleep, name='diet-viewer'),
    path('steps', views.steps, name='diet-viewer'),
    path('steps', views.weight, name='diet-viewer'),
    path('home', views.main, name='diet-viewer'),
    path('block_user', views.block_user, name='block_user'),
    path('get_user_counter', views.get_user_counter, name='get_user_counter'),
    path('check_name', views.check_name, name='check_name'),
    path('compare_name_pass', views.compare_name_pass, name='compare_name_pass'),
    path('add_account', views.add_account, name='add_account'),
    path('get_user', views.get_user, name='get_details'),
    path('get_all', views.get_all, name='get_details'),

]
