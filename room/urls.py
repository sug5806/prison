from .views import show_media, search, detail
from django.urls import path

app_name = 'room'

urlpatterns = [
    path('', show_media, name='list'),
    path('search/', search, name='search'),
    path('detail/<int:pk>/', detail, name='detail'),

]

