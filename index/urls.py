from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "index"

urlpatterns = [
    path("v2/", views.home, name="home"),
    path("v1/introduction/", views.old_version, name="old_version"),
    path("", views.index, name="index")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
