from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('predict/', views.predict, name='predict'),  # Handle the prediction

]
