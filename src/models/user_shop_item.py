from tortoise import fields
from tortoise.models import Model


class UserShopItem(Model):
    id = fields.CharField(max_length=128, pk=True)

    shopItemId = fields.IntField()
    status = fields.CharField(max_length=64)
    level = fields.IntField(null=True)

    userShopId = fields.CharField(max_length=128, null=True)

    class Meta:
        table = "user_shop_items"
