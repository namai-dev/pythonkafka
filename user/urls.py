from django.urls import path
from . import views
urlpatterns = [
    path("", views.Testing.as_view()),
    path("register/", views.UserService.as_view())
    
]
