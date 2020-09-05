from django.urls import path
from . import views

urlpatterns = [
    # path('register/admin', views.registerView, name='Register'),
    # path('', views.loginView, name='Login'),
    path('', views.dashboardView, name='Dashboard'),
    path('register/', views.adminRegister, name='AdminReg'),
    # path('error404/', views.errorView, name='error404'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.adminDetails, name='Details'),
    path('user/<value>/', views.adminDetails, name='DetailsV'),
    path('user/delete/<user>', views.deleteView, name='Delete'),
    path('user/edit/<user>', views.editView, name='Edit'),
    path('approve/', views.approveView, name='Approval'),
    path('approve/admin/', views.approveView, name='AdminApproval'),
    path('approve/<id>/<email>/', views.approve, name='Approve'),
    path('unapprove/<id>/<email>', views.unapprove, name='Unapprove'),
]


