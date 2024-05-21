from django.urls import path
from . import views
from django.urls import register_converter
from utils.convertors import UsernameConverter,MobileConverter

register_converter(UsernameConverter, 'username')
register_converter(MobileConverter, 'mobile')

urlpatterns = [
    path('usernames/<username:username>/count/', views.UsernameCountView.as_view()),
    path('mobiles/<mobile:mobile>/count/', views.MobilecountView.as_view()),
    path('register/', views.RegisterView.as_view()),
]