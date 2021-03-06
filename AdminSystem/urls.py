"""ApplySystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    #url(r'^$', views.index, name='index'),
    url(r'^index/', views.get_index_html),
    url(r'^design/', views.get_front_design_html),
    url(r'^tables/', views.get_tables_html),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^logout/$', views.logout, name = 'logout'),

    
    url(r'^api/get/classes/$', views.get_classes),
    url(r'^api/get/apply/$', views.get_apply),
    url(r'^api/set/classes/$', views.set_classes),

]
