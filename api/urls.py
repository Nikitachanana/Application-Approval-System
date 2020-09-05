from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('token/', views.Registration.as_view(), name='token'),
    path('gentoken/', views.TokenGen.as_view(), name='TokenGen'),
    path('verify/', views.Verify.as_view(), name='Verify'),
]