from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views

urlpatterns = [
    path('about/', views.aboutus, name='aboutus'),
    path('contact/', views.contactus, name='contactus'),
    path('', include('home.urls')),
    path('product/', include('product.urls')),

    path('product/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('category/<int:id>/<slug:slug>',views.category_product, name='category_product'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)