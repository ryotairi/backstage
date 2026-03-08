from tortoise import fields
from tortoise.models import Model


class UserAreaPlaylistStatus(Model):
    id = fields.CharField(max_length=128, pk=True)

    areaPlaylistId = fields.IntField()
    status = fields.CharField(max_length=64)

    class Meta:
        table = "area_playlist_statuses"
