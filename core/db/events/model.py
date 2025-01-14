from dateutil import parser

from core.db.model import BaseModel
from pynamodb.attributes import BooleanAttribute, ListAttribute, MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.constants import STRING
from services.events import constants


class RecurrenceTypeEnumUnicodeAttribute(UnicodeAttribute):
    attr_type = STRING

    def serialize(self, value):
        if not constants.RecurrenceType.has_value(value):
            raise ValueError(
                f"{self.attr_name} must be one of {constants.RecurrenceType.values()}, not '{value}'")
        else:
            return UnicodeAttribute.serialize(self, value)


class OccurrenceTypeEnumUnicodeAttribute(UnicodeAttribute):
    attr_type = STRING

    def serialize(self, value):
        if not constants.OccurrenceType.has_value(value):
            raise ValueError(
                f"{self.attr_name} must be one of {constants.OccurrenceType.values()}, not '{value}'")
        else:
            return UnicodeAttribute.serialize(self, value)


class DateAttribute(UnicodeAttribute):
    """
    This class will serializer/deserialize any date Python object and store as a unicode attribute
    """
    attr_type = STRING

    def serialize(self, value):
        return super(DateAttribute, self).serialize(value.strftime(constants.EVENT_DATE_FORMAT))

    def deserialize(self, value):
        return parser.parse(value)


class TimeAttribute(UnicodeAttribute):
    """
    This class will serializer/deserialize any time Python object and store as a unicode attribute
    """
    attr_type = STRING

    def serialize(self, value):
        return super(TimeAttribute, self).serialize(value.strftime(constants.EVENT_TIME_FORMAT))

    def deserialize(self, value):
        return parser.parse(value)


class RecurrenceDetails(MapAttribute):
    recurrence = RecurrenceTypeEnumUnicodeAttribute()
    occurrence_type = OccurrenceTypeEnumUnicodeAttribute()
    num_recurrences = NumberAttribute()
    on_end_date = DateAttribute(null=True)
    day_of_week = NumberAttribute(null=True)
    week_of_month = NumberAttribute(null=True)
    separation_count = NumberAttribute(default=1)


class OccurrenceDetail(MapAttribute):
    occurrence_num = NumberAttribute()
    start_date = DateAttribute()
    end_date = DateAttribute()


class EventModel(BaseModel):
    class Meta(BaseModel.Meta):
        simple_name = 'event'

    id = UnicodeAttribute(hash_key=True)
    owner = UnicodeAttribute(range_key=True)
    owner_name = UnicodeAttribute(default='')
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    contact_email = UnicodeAttribute(default='')
    categories = ListAttribute(default=lambda: [])
    start_date = DateAttribute()
    end_date = DateAttribute()
    start_time = TimeAttribute()
    end_time = TimeAttribute()
    location = UnicodeAttribute(default='')
    is_recurring = BooleanAttribute(default=False)
    recurrence_details = RecurrenceDetails(null=True, default=lambda: [])
    occurrences = ListAttribute(of=OccurrenceDetail, default=lambda: [])
    timezone = UnicodeAttribute(default='GMT')
