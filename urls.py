"""ProOne URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url,include
from appOne import urls,views

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url('admin/', admin.site.urls),
    url(r'^employees',views.employees),
    url(r'^signup', views.signup),
    url(r'^login', views.loginconnection),
    url(r'^logout', views.logout_view),
url(r'^pendingusers', views.pendingusers),
#url(r'^activate/(?P<submit>(.*))/(?P<username>(.*))/$', views.activate),#giving pattern to a value is that format
url(r'^activate/(?P<userDetails>(.*))/$', views.activate),#giving pattern to a value is that format
    url(r'^forgotpassword', views.forgotpassword),
#url(r'^forgotpassword/(?P<emailid>(.*))/$', views.forgotpassword),
    url(r'^resetpassword/(?P<emailid>(.*))/$', views.changepassword),
    url(r'^setpassword', views.setpassword),
    url(r'^registercomplaint', views.RegisterComplaint),
    url(r'^tickets', views.tickets),
    url(r'^mytickets', views.mytickets),
    url(r'^helpdesk', views.helpdesk),
    url(r'^comments/(?P<complainttitle>(.*))/$', views.comments),
    url(r'^Addcomment/(?P<complainttitle>(.*))/$', views.Addcomment),
    url(r'^savecomment/(?P<complainttitle>(.*))/$', views.savecomment),
    url(r'^assignedtickets', views.assignedtickets),
    url(r'^assignment/(?P<complaintDetails>(.*))/$', views.assignment),
    url(r'^close/(?P<complaintid>(.*))/$', views.close),
    url(r'^close1/(?P<complaintid>(.*))/$', views.close1),

]
