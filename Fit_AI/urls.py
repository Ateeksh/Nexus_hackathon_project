from django.urls import path
from . import views 

urlpatterns = [
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('assistant', views.Ai, name='assistant'),
    path('register', views.register, name='login'),
    path('Nutrient_counter', views.scan, name='Calories'),
    path('scan/', views.file_upload, name='Nutrient_checker'),
    path('diet', views.diet, name='diet-viewer'),
    path('gdiet', views.diet, name='diet-viewer'),

]
