from tortoise import fields
from tortoise.models import Model


class UserBoostStatus(Model):
    userId = fields.BigIntField(unique=True)
    current = fields.IntField()
    recoveryAt = fields.DatetimeField()

    class Meta:
        table = "users_boost"
