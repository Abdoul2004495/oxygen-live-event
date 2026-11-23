"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
# A ready-made view that only displays a template (no logic needed for now)
from django.views.generic import TemplateView
from django.conf import settings                  # access to settings.py values
from django.conf.urls.static import static       # helper that serves uploaded files in development



urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    # The empty address "" is the home page; the name "home" lets us refer to it
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:                                                    # only while developing
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # serve /media/ from the media folder