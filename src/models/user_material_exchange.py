from tortoise import fields
from tortoise.models import Model


class UserMaterialExchange(Model):
    id = fields.CharField(max_length=128, pk=True)

    userId = fields.BigIntField()
    materialExchangeId = fields.IntField()
    exchangeCount = fields.IntField()
    totalExchangeCount = fields.IntField()
    lastExchangedAt = fields.DatetimeField(auto_now_add=True)
    exchangeStatus = fields.CharField(max_length=32)  # exchangeable, out_period, not_exchangeable
    exchangeRemaining = fields.IntField(null=True)
    refreshedAt = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_material_exchanges"
