from tortoise import fields
from tortoise.models import Model


class UserMusicResult(Model):
    uniqueResultId = fields.CharField(max_length=128, pk=True)

    userId = fields.BigIntField()
    musicId = fields.IntField()
    musicDifficulty = fields.CharField(max_length=32)  # easy, normal, hard, expert, master, append
    playType = fields.CharField(max_length=32, default="solo")
    playResult = fields.CharField(max_length=32)  # not_clear, clear
    highScore = fields.IntField()
    fullComboFlg = fields.BooleanField()
    fullPerfectFlg = fields.BooleanField()
    mvpCount = fields.IntField()
    superStarCount = fields.IntField()

    createdAt = fields.DatetimeField(auto_now_add=True)
    updatedAt = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_music_results"
