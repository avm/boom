from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:game_id>/add_cards', views.add_cards, name='add_cards'),
    path('<str:game_id>', views.game, name='game'),
]
