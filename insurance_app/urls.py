from django.urls import path
from .views import get_quote, create_quote

urlpatterns = [
    path('quote/<int:quote_id>/', get_quote, name='get_quote'),
    path('quote/', create_quote, name='create_quote'),
]
