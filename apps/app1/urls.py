from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_register),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    # path('checkout', views.checkout),
    # path('refresh_checkout', views.refresh_checkout)
]