from tortoise import fields
from tortoise.models import Model


class UserShop(Model):
    id = fields.CharField(max_length=128, pk=True)

    shopId = fields.IntField()
    userId = fields.BigIntField(null=True)

    class Meta:
        table = "user_shops"
