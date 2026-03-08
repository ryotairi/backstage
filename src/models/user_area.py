from tortoise import fields
from tortoise.models import Model


class UserArea(Model):
    id = fields.CharField(max_length=128, pk=True)

    userId = fields.BigIntField()

    status = fields.CharField(max_length=32)  # released, unreleased
    areaId = fields.IntField()

    actionSets = fields.JSONField(default=[])
    areaItems = fields.JSONField(default=[])

    areaPlaylistStatusId = fields.CharField(max_length=128, null=True)

    class Meta:
        table = "user_areas"
