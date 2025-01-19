"""
URL configuration for gas_utility_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from customer_service import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Customer Service URLs
    path('', views.home, name='home'),  # Homepage of the customer service section
    path('submit-request/', views.submit_request, name='submit_request'),  # Form to submit a service request
    path('request-status/', views.request_status, name='request_status'),  # Track request status
    path('account-info/', views.account_info, name='account_info'),  # View account info (if necessary)
    
    # Home Page URL (root URL)
    
    
    path('register/', views.register, name='register'),

    # Authentication URLs (Login and Logout)
    path('login/', auth_views.LoginView.as_view(template_name='customer_service/login.html'), name='login'),
 # Login page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout page
    
    # Support Dashboard URLs
    path('support/dashboard/', views.support_dashboard, name='support_dashboard'),  # Support team dashboard
    path('support/update-request/<int:request_id>/', views.update_request_status, name='update_request_status'),  # Update a request status

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
