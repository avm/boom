from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Game, Card

import random

def index(request):
	game_id = hex(random.randint(2**24, 2**32 - 1))[2:]
	return redirect('game', game_id)

def game(request, game_id):
	game, created = Game.objects.get_or_create(slug=game_id)
	return render(request, 'boom/game.html', {'game': game})

def add_cards(request, game_id):
	game, created = Game.objects.get_or_create(slug=game_id)
	text = request.POST['cards']
	Card.objects.bulk_create([
		Card(game=game, name=name, order=0, winning_team=0) for name in
			(line.strip() for line in text.split('\n'))
			if name != ''
	])
	return redirect('game', game_id=game_id)

def start_game(request, game_id):
	game, created = Game.objects.get_or_create(slug=game_id)
	if game.state == Game.State.POPULATING:
		game.state = Game.State.PLAYING
