

from os import stat
from django.contrib import admin
from django.urls import path,include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from django.views.generic import TemplateView

urlpatterns = [
    
    path('users/',include('users.urls')),
    path('feed/',include('posts.urls')),
    path('events/',include('events.urls')),
    path('donations/',include('donations.urls')),
    path('transactions/',include('transactions.urls')),
    
    
    



     # static
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
