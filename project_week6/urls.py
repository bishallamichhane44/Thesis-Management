"""
URL configuration for project_week6 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
# from app_week6 import views

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path('', views.home, name='home'),
#     path('theses/<int:thesis_id>/', views.thesis_details, name='thesis_details'),
#     path('thesis_list', views.thesis_list, name='thesis_list'),
#     path('about/', views.about, name="about")
# ]
from django.contrib import admin
from django.urls import path
from app_week6 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('upload_thesis/', views.upload_thesis, name='upload_thesis'),
    path('approve_thesis/', views.approve_thesis, name='approve_thesis'),
    path('view_theses/', views.view_theses, name='view_theses'),
    path('create_group/', views.create_group, name='create_group'),
    path('approve/<int:thesis_id>/', views.approve, name='approve'),
    path('request_to_join/<int:thesis_id>/', views.request_join, name='request_to_join'),
    path('view_theses/<int:thesis_id>/', views.thesis_detail, name='view_theses'),
    path('approve_student/<int:thesis_id>/<int:student_id>/', views.approve_student, name='approve_student'),
    
]


