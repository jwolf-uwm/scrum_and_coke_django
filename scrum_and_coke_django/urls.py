"""scrum_and_coke_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from ta_assign.views import Command, CreateAccount, CreateCourse, Index, Login, Logout, AccessInfo

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  path('', Index.as_view(), name='index1'),
  path('index/', Index.as_view(), name='index1'),
  path('create_account/', CreateAccount.as_view(), name='CreateAccount1'),
  path('create_course/', CreateCourse.as_view(), name='CreateCourse1'),
  path('command/', Command.as_view(), name='Command1'),
  path('login/', Login.as_view(), name='Login1'),
  path('logout/', Logout.as_view(), name='Logout1'),
  path('access_info/', AccessInfo.as_view(), name='AccessInfo1')
]
