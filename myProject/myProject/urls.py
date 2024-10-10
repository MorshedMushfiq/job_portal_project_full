"""
URL configuration for myProject project.

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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginPage, name='loginPage'),
    path('logout/', logoutPage, name='logoutPage'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('edit_basic_info/<int:id>', edit_basic_info, name='edit_basic_info'),
    path('add_basic_info/', add_basic_info, name='add_basic_info'),
    path('add_job/', add_job, name='add_job'),
    path('job_feed/', job_feed, name='job_feed'),
    path('apply_now/<int:id>', apply_now, name="apply_now"),
    path('view_job/<int:id>', apply_now, name="view_job"),
    path('created_job_by_recruiter/', createdJobByRecruiter, name='created_job_by_recruiter'),
    path('job_delete/<int:id>', job_delete, name='job_delete'),
    path('job_edit/<int:id>', job_edit, name='job_edit'),
    path('applied_jobs/', applied_jobs, name='applied_jobs'),
    path('view_application/<int:id>', view_application, name='view_application'),
    path('delete_applications/<int:id>', delete_applications, name='delete_applications'),
    path('my_settings/', my_settings, name='my_settings'),
    path('add_education/', add_education, name='add_education'),
    path('delete_education/<int:id>', deleteEducation, name='delete_education'),
    path('edit_education/<int:id>', editEducation, name='edit_education'),
    path('add_experience/', addExperience, name='add_experience'),
    path('delete_experience/<int:id>', deleteExperience, name='delete_experience'),
    path('edit_experience/<int:id>', editExperience, name='edit_experience'),
    path('add_skills/', add_skills, name='add_skills'),
    path('delete_skill/<int:id>', deleteSkill, name='delete_skill'),
    path('edit_skill/<int:id>', edit_skills, name='edit_skill'),
    path('add_language/', addLanguage, name='add_language'),
    path('delete_language/<int:id>', deleteLanguage, name='delete_language'),
    path('edit_language/<int:id>', editLanguage, name='edit_language'),
    path('add_interest/', addInterest, name='add_interest'),
    path('delete_interest/<int:id>', deleteInterest, name='delete_interest'),
    path('edit_interest/<int:id>', editInterest, name='edit_interest'),
    path('search/', search_job, name="search_job"),
    path('change_password/', changePassword, name='change_password'),
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
