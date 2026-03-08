from tortoise import fields
from tortoise.models import Model


class UserGameData(Model):
    userId = fields.BigIntField(unique=True)

    deck = fields.IntField(default=1)
    rank = fields.IntField(default=1)
    exp = fields.IntField(default=0)
    totalExp = fields.IntField(default=0)
    coin = fields.IntField(default=0)
    virtualCoin = fields.IntField(default=0)
    crystals = fields.IntField(default=10000)

    eventArchiveCompleteReadRewards = fields.JSONField(default=[])

    class Meta:
        table = "users_game_data"
