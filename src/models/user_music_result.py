from tortoise import fields
from tortoise.models import Model


class UserMusicResult(Model):
    
    userId = fields.BigIntField()
    musicId = fields.IntField()
    musicDifficulty = fields.CharField(max_length=32)  # easy, normal, hard, expert, master, append
    playType = fields.CharField(max_length=32, default="solo")
    playResult = fields.CharField(max_length=32)  # not_clear, clear, full_combo, full_perfect
    highScore = fields.IntField()
    fullComboFlg = fields.BooleanField()
    fullPerfectFlg = fields.BooleanField()
    mvpCount = fields.IntField(default=0)
    superStarCount = fields.IntField(default=0)

    createdAt = fields.DatetimeField(auto_now_add=True) # it's createAt in Sekai.UserMusicResult 
    updatedAt = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_music_results"
