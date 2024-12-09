from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),  # Ensure this path is mapped
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard URL
    path('export-csv/', views.export_users_csv, name='export_users_csv'),  # Add this URL for exporting CSV
    path('logout/', LogoutView.as_view(), name='logout'),
]