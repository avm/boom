from django.db import models
import json


class Game(models.Model):
    class State(models.TextChoices):
        POPULATING = 'po', ('Populating')
        PLAYING = 'pl', ('Playing')
        FINISHED = 'fi', ('Finished')

    slug = models.CharField(max_length=20)
    state = models.CharField(
        max_length=2,
        choices=State.choices,
        default=State.POPULATING,
    )

    def card_count(self):
        return self.card_set.all().count()

    def get_scores(self):
        scores = list(self.score_set.all().order_by('team_id').values())
        last_id = scores[-1].team_id if scores else 0
        scores.append({'team_id': last_id+1, 'value': 0})
        return scores

    def get_active_cards(self):
        return list(self.card_set.filter(winning_team=0).order_by('order').values('id', 'name'))


class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_id = models.IntegerField()
    value = models.IntegerField()
    

class Card(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    order = models.IntegerField()
    winning_team = models.IntegerField()
