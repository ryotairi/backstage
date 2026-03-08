from tortoise import fields
from tortoise.models import Model


class UserCharacter(Model):
    uniqueCharacterId = fields.CharField(max_length=128, pk=True)

    userId = fields.BigIntField()
    characterId = fields.IntField()
    characterRank = fields.IntField(default=1)
    exp = fields.IntField(default=0)
    totalExp = fields.IntField(default=0)

    class Meta:
        table = "user_characters"
