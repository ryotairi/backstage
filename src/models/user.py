from tortoise import fields
from tortoise.models import Model


class User(Model):
    userId = fields.BigIntField(unique=True)
    credential = fields.CharField(max_length=512)

    signature = fields.CharField(max_length=512)
    platform = fields.CharField(max_length=64)
    deviceModel = fields.CharField(max_length=128)
    operatingSystem = fields.CharField(max_length=128)

    birthdate = fields.DatetimeField(null=True)

    registeredAt = fields.DatetimeField(auto_now_add=True)

    tutorialStatus = fields.CharField(max_length=64, default="start")
    userLiveId = fields.CharField(max_length=128, null=True)

    name = fields.CharField(max_length=128)

    class Meta:
        table = "users"
