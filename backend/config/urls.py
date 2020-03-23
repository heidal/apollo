"""backend URL Configuration

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

apipatterns = []

if settings.DEBUG:
    import debug_toolbar

    apipatterns += [path("__debug__/", include(debug_toolbar.urls))]

apipatterns += [
    path("admin/", admin.site.urls),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("users/", include("apollo.users.urls", namespace="users")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [path("api/", include(apipatterns))]
