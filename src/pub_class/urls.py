"""pub_class URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^postsign/', views.postsign),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^register/', views.register, name="register"),
    url(r'^postsignup/', views.postsignup, name="postsignup"),
    url(r'^index/', views.index, name="index"),
    url(r'^create/', views.create, name='create'),
    url(r'^post_create/', views.post_create, name='post_create'),
    url(r'^check/', views.check, name='check'),
    url(r'^post_check/', views.post_check, name='post_check'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^publications/', views.publications, name='publications'),
    url(r'^phrases/(?P<pid>\d+)/$', views.phrases, name='phrases'),
    url(r'^update', views.update, name='update'),
    url(r'^abstracts', views.abstract, name='abstracts'),
    url(r'^predicts/(?P<pid>\d+)/$', views.predicts, name='predicts')
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

