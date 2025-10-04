"""config URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from config import settings
import core.urls
from user import views
import user.urls
from django.conf.urls.static import static

MEDIA_FILE_PATHS = static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

urlpatterns = [
    path('admin/',admin.site.urls),
    path('user/', include(user.urls, namespace='user')), 
    path('', include('core.urls', namespace='core')),
    path('movie/<int:movie_id>/vote', views.CreateVote.as_view(), name='CreateVote'),
    path('movie/<int:movie_id>/vote/<int:pk>', views.UpdateVote.as_view(), name='UpdateVote'),

] + MEDIA_FILE_PATHS
