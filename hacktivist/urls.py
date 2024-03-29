from django.urls import path
from.import views

urlpatterns = [
path('login/', views.Login, name="Login"),
path('signup/', views.Signup, name="Signup"),
path('logout/', views.Logout, name="Logout"),
path('forget-password/', views.ForgetPassword, name="ForgetPassword"),
path('change-password/<token>/', views.ChangePassword, name="ChangePassword"),
] 