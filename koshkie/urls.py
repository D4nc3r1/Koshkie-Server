#  Copyright (c) Code Written and Tested by Ahmed Emad in 02/02/2020, 00:34
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from koshkie.views import logout_view

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('logout/', logout_view, name='logout'),
                  path('users/', include('users.urls')),
                  path('drivers/', include('drivers.urls')),
                  path('shops/', include('shops.urls')),
                  path('orders/', include('orders.urls'))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
