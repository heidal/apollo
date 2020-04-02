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
    path("api-auth/", include("rest_framework.urls")),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("users/", include("apollo.users.urls", namespace="users")),
    path("elections/", include("apollo.elections.urls", namespace="elections")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [path("api/", include(apipatterns))]
