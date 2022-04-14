from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("jet/", include("jet.urls", "jet")),
    
    path('api/v1/products/',include('apps.products.urls')),
    path('api/v1/accounts/',include('apps.accounts.urls')),
]


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Django Shop",
      default_version='v1',
      contact=openapi.Contact(email="danilovhamza@mail.ru"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
