from tortoise import fields
from tortoise.models import Model


class UserMusic(Model):
    uniqueMusicId = fields.CharField(max_length=128, pk=True)

    userId = fields.BigIntField()
    musicId = fields.IntField()

    vocals = fields.JSONField(default=[])
    availableDifficulties = fields.JSONField(default=["easy", "normal", "hard", "expert"])

    createdAt = fields.DatetimeField(auto_now_add=True)
    updatedAt = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_musics"
