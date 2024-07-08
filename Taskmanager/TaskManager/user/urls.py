from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.login,name="login"),
    path('logout/', views.logout,name="logout"),
    path('session/', views.session,name="session"),
    path('whoami/', views.whoami,name="whoami"),
]