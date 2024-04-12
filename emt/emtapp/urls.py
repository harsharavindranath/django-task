from django.urls import path
from .import views

urlpatterns = [
    path('userregister/',views.user_registration),
    path('userlogin/',views.userlogin),
    # path('employeehomepage/<int:id>/',views.employeehomepage),
   
    path('admin_homepage/',views.admin_homepage),
]