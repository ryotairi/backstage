from tortoise import Model, fields

from src.enum.friend_request_scope_enum import FriendRequestScope
from src.enum.music_type_enum import MusicTypeEnum


class UserConfig(Model):
    userId = fields.BigIntField(primary_key=True)
    
    defaultMusicType = fields.CharEnumField(MusicTypeEnum)
    displayLoginStatus = fields.BooleanField()
    friendRequestScope = fields.CharEnumField(FriendRequestScope)
    
    class Meta:
        table = "user_configs"