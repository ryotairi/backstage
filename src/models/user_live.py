from tortoise import fields
from tortoise.models import Model


class UserLive(Model):
    userId = fields.BigIntField(unique=True)

    liveId = fields.CharField(max_length=128)

    musicId = fields.IntField()
    musicDifficultyId = fields.IntField()
    musicVocalId = fields.IntField()
    deckId = fields.IntField()
    boostCount = fields.IntField()
    isAutoPlay = fields.BooleanField()
    
    # musicDifficulty = fields.CharField(max_length=16)

    # has results only after finishing
    perfectCount = fields.IntField(null=True)
    greatCount = fields.IntField(null=True)
    goodCount = fields.IntField(null=True)
    badCount = fields.IntField(null=True)
    missCount = fields.IntField(null=True)
    score = fields.IntField(null=True)
    life = fields.IntField(null=True)
    maxCombo = fields.IntField(null=True)
    tapCount = fields.IntField(null=True)

    class Meta:
        table = "users_live"
