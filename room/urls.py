from .views import showmedia, search
from django.urls import path

app_name = 'room'

urlpatterns = [
    path('', showmedia, name='list'),
    path('search/', search, name='search')

]

