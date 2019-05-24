from .views import showmedia
from django.urls import path

app_name = 'room'

urlpatterns = [
    path('', showmedia, name='list'),

]

