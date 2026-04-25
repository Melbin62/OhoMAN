"""
URL configuration for OhoMAN project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from OhoMANApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('customer_registration/', views.customer_registration),
    path('serviceprov_registration/', views.serviceprov_registration),
    path('login/', views.login),
    path('',views.profile),
    path('logout/', views.logout),

    path('servicepov_req/', views.servicepov_req),
    path('approved_providers/',views.approved_providers),
    path('view_approvedpov/', views.view_approvedpov),
    path('reject_providers/',views.reject_providers),
    path('remove_approvepov/',views.remove_approvepov),
    path('add_service/', views.add_service),
    path('remove_service/',views.remove_service),

    path('servicebooking_req/',views.servicebooking_req),
    path('confirmed_booking/',views.confirmed_booking),
    path('service_booking/', views.service_booking),
    path('booking_form/', views.booking_form),
    path('booking_req/',views.booking_req),
    path('booking_status/',views.booking_status),
    path('approve_booking/',views.approve_booking),
    path('reject_booking/',views.reject_booking),
    path('confirm_pay/',views.confirm_pay),
    path('success/',views.success),
    path('save_rating/',views.save_rating),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
