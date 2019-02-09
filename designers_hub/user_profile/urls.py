from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('home/', views.home,name='home'),    
    path('designers/<str:username>/', views.designer_profile, name="designer_profile"),
    path('clients/<str:username>/', views.client_profile, name="client_profile"), 
    path('designers/<str:username>/projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('designers/<str:username>/update_profile/', views.update_profile, name='settings'),
    path('designers/<str:username>/upload-portfolio/', views.upload_portfolio, name='upload_portfolio'),  
    path('designers/<str:username>/projects/<int:pk>/', views.project_detail, name='project-details'),
    path('search/', views.search_data,name="search"),
]
