from tortoise import fields
from tortoise.models import Model


class UserStamp(Model):
    id = fields.CharField(max_length=128, pk=True)

    stampId = fields.IntField()
    obtainedAt = fields.DatetimeField(auto_now_add=True)

    userId = fields.BigIntField()

    class Meta:
        table = "user_stamps"
