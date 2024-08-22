from django.urls import path
from .views import send_orders_report

urlpatterns = [
    path('send_report/', send_orders_report, name='send_orders_report'),

]
