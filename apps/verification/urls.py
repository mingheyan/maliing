from django.urls import path
from . import views
from utils.convertors import UUIDConverter,MobileConverter
from django.urls import register_converter

register_converter(UUIDConverter, 'uuid')
register_converter(MobileConverter, 'mobile')



urlpatterns = [
    path("image_codes/<uuid:uuid>/",views.ImageCodeView.as_view()),
    path('sms_codes/<mobile:mobile>/', views.SmsCodeView.as_view())
]