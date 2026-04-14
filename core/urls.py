from django.urls import path
from .views import login_view, galeria_view, logout_view

urlpatterns = [
    path('', login_view, name='login'),
    path('galeria/', galeria_view, name='galeria'),
    path('logout/', logout_view, name='logout'),
]                    