from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('checkout/', views.checkout, name="checkout"),
    path('tracker/', views.tracker, name="tracker"),
]