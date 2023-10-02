from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

# API URLS
urlpatterns = [
    # API base url
    path("api/v1/", include("config.api_router")),
    # DRF auth token
    path("api-auth/", include("rest_framework.urls")),
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    # Document upload url
    path("api/v1/docs", include("uploader.urls")),
    # Document get url, any path the user chooses to see the document in
    ## doc reference for this setting : https://stackoverflow.com/questions/51084909/how-can-i-use-a-catch-all-route-using-path-or-re-path-so-that-django-passes
    # path("/api/o", include("uploader.urls")),
    # # path("<path:resource>", include("uploader.urls")),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
