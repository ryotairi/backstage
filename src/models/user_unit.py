from tortoise import fields
from tortoise.models import Model


class UserUnit(Model):
    uniqueUnitId = fields.CharField(max_length=128, pk=True)

    userId = fields.BigIntField()
    unit = fields.CharField(max_length=32)  # idol, light_sound, none, piapro, school_refusal, street, theme_park
    rank = fields.IntField(default=1)
    exp = fields.IntField(default=0)
    totalExp = fields.IntField(default=0)
    userGameDataUserId = fields.BigIntField(null=True)

    class Meta:
        table = "user_units"
