from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import settings
from user_profile import views as user_views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from user_profile import views


urlpatterns = [
    path('', include('user_profile.urls')),
    path('admin/', admin.site.urls),
    path('contracts/', include('contract.urls')),
    path('chats/', include('chat.urls')),

    path('payments/', include('payment.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.SignUpView.as_view(), name='register'),
    path('accounts/register/designer/', views.DesignerSignUpView.as_view(), name='designer_register'),
    path('accounts/register/client/', views.ClientSignUpView.as_view(), name='client_register'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    
    path('events/', include('event.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='user_profile/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='user_profile/logout.html'), name='logout'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)