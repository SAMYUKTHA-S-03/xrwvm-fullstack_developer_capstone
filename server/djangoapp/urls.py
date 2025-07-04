from django.urls import path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),  # Add this line
    # other paths...
]
