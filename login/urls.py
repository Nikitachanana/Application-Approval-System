from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('', views.login, name='Login'),
    # path('logout/', views.logout, name='logout'),
    path('404/', views.error404, name='404'),
    path('delete/', views.delete, name='Delete'),
    path('verify/', views.verifyOTP, name='verifyOTP'),
    path('forgot/', views.forgot, name='forgot'),
    path('activate/<token>/<ptoken>', views.activate, name='activate'),
    path('resetpassword/', views.resetPassword, name='resetPassword'),
    #path('test/', views.test, name='test'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)