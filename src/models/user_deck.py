from tortoise import fields
from tortoise.models import Model


class UserDeck(Model):
    uniqueDeckId = fields.CharField(max_length=128, pk=True)

    userId = fields.BigIntField()
    deckId = fields.IntField()
    name = fields.CharField(max_length=128)
    members = fields.JSONField(default=[])  # member1, member2, member3, member4, member5

    class Meta:
        table = "user_decks"
