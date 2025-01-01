from django.urls import path
from . import views

urlpatterns = [
    path('get-market-data/', views.get_market_data, name='get_market_data'),
]
