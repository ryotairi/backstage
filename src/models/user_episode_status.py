from tortoise import fields
from tortoise.models import Model


class UserEpisodeStatus(Model):
    id = fields.CharField(max_length=128, pk=True)

    storyType = fields.CharField(max_length=64)  # unit_story, special_story, card_story, character_profile_story, event_story, archive_event_story
    episodeId = fields.IntField()
    status = fields.CharField(max_length=32)  # can_not_read, unreleased, released, already_read
    isNotSkipped = fields.BooleanField()

    userId = fields.BigIntField(null=True)

    class Meta:
        table = "user_episode_statuses"
