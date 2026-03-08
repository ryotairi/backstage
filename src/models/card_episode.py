from tortoise import fields
from tortoise.models import Model


class CardEpisode(Model):
    id = fields.CharField(max_length=128, pk=True)

    cardEpisodeId = fields.IntField()
    scenarioStatus = fields.CharField(max_length=32)  # unreleased
    scenarioStatusReasons = fields.JSONField(default=[])
    isNotSkipped = fields.BooleanField()
    cardId = fields.CharField(max_length=128, null=True)

    class Meta:
        table = "card_episodes"
