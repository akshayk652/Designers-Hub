from django.urls import path
from . import views

urlpatterns = [
    path('', views.contracts_list, name="contracts-list"),
    path('<int:pk>/', views.contract_details, name='contract-details'),
    path('new/', views.contract_create_form, name="contract-form"),
    path('upload/<int:pk>', views.upload_file, name='contract-upload'),
    path("download/<int:pk>/", views.download, name='download'),
    path("delete/<int:pk>", views.delete_contract, name='delete_contract'),
    path("complete/<int:pk>", views.complete_contract, name='complete_contract'),
    path("email/", views.email, name='email'),
    path("ratings/<int:pk>", views.rating, name='contract-rating'),
    path("<str:designer_name>/rating", views.get_rating, name='get_rating'),
]

