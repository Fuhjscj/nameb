import enum
from tortoise import Model, fields


class Chat(Model):
    class ChangeType(enum.Enum):
        DAY = enum.auto()
        NIGTH = enum.auto()


    id: int = fields.IntField(pk=True)
    day_name: str = fields.TextField(null=True)
    nigth_name: str = fields.TextField(null=True)
    is_active: bool = fields.BooleanField(default=False)
    

    def can_change(self, change_type: ChangeType) -> bool:
        if change_type == self.ChangeType.DAY:
            return self.is_active and self.day_name
        else:
            return self.is_active and self.nigth_name 