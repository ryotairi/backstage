from tortoise import Model, fields


class UserMaterial(Model):
    id = fields.IntField(primary_key=True)
    
    userId = fields.BigIntField()
    materialId = fields.IntField()
    quantity = fields.IntField()
    
    class Meta:
        table = 'user_materials'