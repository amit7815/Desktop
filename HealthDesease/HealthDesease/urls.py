"""HealthDesease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from healthapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name="home"),
    path('patient_home', Patient_Home,name="patient_home"),  # USER
    path('doctor_home', Doctor_Home,name="doctor_home"),
    path('admin_home', Admin_Home,name="admin_home"),
    path('login', Login_User,name="login"),
    path('login_admin', Login_admin,name="login_admin"),
    path('signup', Signup_User,name="signup"),
    path('logout', Logout,name="logout"),
    path('add_heartdetail', add_heartdetail,name="add_heartdetail"),
    path('view_history', view_history,name="view_search_pat"),

    path('view_doctor', View_Doctor,name="view_doctor"),
    path('add_doctor', add_doctor,name="add_doctor"),
    path('change_doctor/<int:pid>/', add_doctor,name="change_doctor"),
    path('view_patient', View_Patient,name="view_patient"),
    path('view_feedback', View_Feedback,name="view_feedback"),
    path('edit_profile', Edit_My_deatail,name="edit_profile"),
    path('profile_doctor', Profile_Doctor,name="profile_doctor"),  #user
    path('sent_feedback', sent_feedback,name="sent_feedback"),

    path('delete_searched/<int:pid>', delete_searched, name="delete_searched"),
    path('delete_doctor<int:pid>', delete_doctor, name="delete_doctor"),
    path('assign_status<int:pid>', assign_status, name="assign_status"),
    path('delete_patient<int:pid>', delete_patient, name="delete_patient"),
    path('delete_feedback<int:pid>', delete_feedback, name="delete_feedback"),
    path('predict_desease/<str:pred>/<str:accuracy>/', predict_desease, name="predict_desease"),

    path('add_genralhealth', add_genralhealth, name="add_genralhealth"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
