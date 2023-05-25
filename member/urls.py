"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from.import views

app_name="member"
urlpatterns = [
    path("write/", views.write), #회원가입폼으로 이동
    path("save/", views.save),  #회원가입
    path("idcheck/", views.idcheck), #아이디중복체크
    path("logon/", views.logon), #페이지이동용
    path("logon_proc/", views.logon_proc),#로그온처리
    path("logout_proc/", views.logout_proc),#로그아웃처리
]