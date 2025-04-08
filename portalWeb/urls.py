from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('buildDeck', views.buildDeck, name='buildDeck'),
   path('searchCard/<str:cardInput>/', views.searchCard, name='searchCard'),
]
