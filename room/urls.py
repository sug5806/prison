from .views import showmedia, search, detail
from django.urls import path

app_name = 'room'

urlpatterns = [
    path('', showmedia, name='list'),
    path('search/', search, name='search'),
    path('detail/<int:pk>/', detail, name='detail'),

]

