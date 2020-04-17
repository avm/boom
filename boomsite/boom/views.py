from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Max
from .models import Game, Card, Score

import random
import json


def index(request):
	game_id = hex(random.randint(2**24, 2**32 - 1))[2:]
	return redirect('game', game_id)


def game(request, game_id):
	game, created = Game.objects.get_or_create(slug=game_id)
	if game.state == Game.State.PLAYING:
		template_name = 'boom/stats.html'
	else:
		template_name = 'boom/game.html'
	return render(request, template_name, {'game': game})


def add_cards(request, game_id):
	game, created = Game.objects.get_or_create(slug=game_id)
	text = request.POST['cards']
	Card.objects.bulk_create([
		Card(game=game, name=name, order=0, winning_team=0) for name in
			(line.strip() for line in text.split('\n'))
			if name != ''
	])
	return redirect('game', game_id)


def start_game(request, game_id):
	game, created = Game.objects.get_or_create(slug=game_id)
	if game.card_count() < 4:
		messages.add_message(request, messages.ERROR, 'Not enough cards to start game.')
	elif game.state == Game.State.POPULATING:
		game.state = Game.State.PLAYING
		game.start_set()
		game.save()
	return redirect('game', game_id)


def start_round(request, game_id, team_id):
	game = get_object_or_404(Game, slug=game_id)
	return render(request, 'boom/round.html', {'game': game, 'our_team': team_id})


def win_card(request):
	body = json.loads(request.body)
	win_card = body.get('win_card')
	if win_card is not None:
		card = get_object_or_404(Card, pk=win_card)
		team = body.get('our_team')
		card.winning_team = team
		score, created = Score.objects.get_or_create(game=card.game, team_id=team, defaults=dict(value=0))
		score.value += 1
		score.save()
		card.save()
		remaining = card.game.card_set.filter(winning_team=0).count()
		if remaining == 0:
			card.game.start_set()
			card.game.save()
	show_card = body.get('show_card')
	if show_card:
		# Move it into the back of the deck
		card = get_object_or_404(Card, pk=show_card)
		max_order = card.game.card_set.filter(winning_team=0).aggregate(Max('order'))['order__max']
		card.order = max_order + 1
		card.save()
	return HttpResponse('ok')
