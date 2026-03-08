from tortoise import fields
from tortoise.models import Model


class Card(Model):
    id = fields.CharField(max_length=128, pk=True)

    userId = fields.BigIntField()
    cardId = fields.IntField()
    level = fields.IntField()
    exp = fields.IntField()
    totalExp = fields.IntField()
    skillLevel = fields.IntField()
    skillExp = fields.IntField()
    totalSkillExp = fields.IntField()
    masterRank = fields.IntField()
    specialTrainingStatus = fields.CharField(max_length=32)  # not_doing
    defaultImage = fields.CharField(max_length=32)  # original
    duplicateCount = fields.IntField()
    createdAt = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "cards"
