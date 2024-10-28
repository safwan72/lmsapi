
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns,static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('App_Login.urls')),
    path('work2/', include('App_Work2.urls')),
    path('blog/', include('App_Blog.urls')),
]

urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)