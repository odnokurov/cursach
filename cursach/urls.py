from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
path('admin/', admin.site.urls),
path('catalog/', include('catalog.urls')),
path('', RedirectView.as_view(url='/catalog/', permanent=True)),

path('accounts/logout/', LogoutView.as_view(http_method_names=['get', 'post'], next_page='/catalog/'),
    name='logout'),
path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

