from django.db import models


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
