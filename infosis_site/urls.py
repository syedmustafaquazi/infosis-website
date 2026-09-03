from django.contrib import admin
from django.urls import path
from enquiries import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('details/', views.details, name='details'),
    path('api/enquiries/', views.create_enquiry, name='create_enquiry'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('dashboard/enquiries/<int:pk>/status/', views.update_status, name='update_status'),
    path('dashboard/enquiries/<int:pk>/delete/', views.delete_enquiry, name='delete_enquiry'),
]
