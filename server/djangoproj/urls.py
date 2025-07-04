from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API paths for your Django app
    path('djangoapp/', include('djangoapp.urls')),

    # Serve React single page app at these routes
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('', TemplateView.as_view(template_name="home.html")),

]
