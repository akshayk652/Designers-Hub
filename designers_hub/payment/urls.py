from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
   path('',views.payment_process, name='payments'),
   path('payment_done/', TemplateView.as_view(template_name='payment/payment_done.html'), name='payment_done'),
   path('payment_canceled/', TemplateView.as_view(template_name='payment/payment_canceled.html'), name='payment_canceled'),
]
