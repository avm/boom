from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('win', views.win_card, name='win_card'),
    path('<str:game_id>/add_cards', views.add_cards, name='add_cards'),
    path('<str:game_id>', views.game, name='game'),
    path('<str:game_id>/start', views.start_game, name='start_game'),
    path('<str:game_id>/start_round/<int:team_id>', views.start_round, name='start_round'),
]
