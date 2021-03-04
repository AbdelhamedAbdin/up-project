from django.contrib import admin
from django.urls import path, include
from django.urls import reverse_lazy


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('v2/introduction/', include('introduction.urls')),
    path('v2/search/', include('corpus_search.urls')),
    path('v2/', include('list_app.urls')),
    path('accounts/', include('accounts.urls')),
]

