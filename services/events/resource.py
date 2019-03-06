from core.resource import ma
from marshmallow import fields, ValidationError
from services.events import constants


def validate_recurrence(val):
    if not constants.RecurrenceType.has_value(val):
        raise ValidationError('Invalid value, must be one of {}'.format(constants.RecurrenceType.values()))


def validate_update_type(val):
    if not constants.UpdateType.has_value(val):
        raise ValidationError('Invalid value, must be one of {}'.format(constants.UpdateType.values()))


# TODO Check and see why val limits do not work
class RecurrenceDetails(ma.Schema):
    recurrence = fields.Str(required=True, validate=validate_recurrence)
    num_recurrences = fields.Int(required=True,
                                 validate=lambda val: constants.MIN_RECURRENCE <= val <= constants.MAX_RECURRENCE)
    nday = fields.Int(required=True, validate=lambda val: 0 <= val <= 7)  # 0 value when not needed for NWEEKDAY
    nweek = fields.Int(required=True, validate=lambda val: [0, 1, 2, 3, 4, 5, -1])  # 0 value when not needed for NWEEKDAY

    # day_of_week = fields.Int(required=False, validate=lambda val: 1 <= val <= 7)
    # week_of_month = fields.Int(required=False, validate=lambda val: 1 <= val <= 4)
    # day_of_month = fields.Int(required=False, validate=lambda val: 1 <= val <= 31)
    # days_of_week = fields.List(fields.Int(), validate=lambda val: 1 <= val <= 7, required=False)

    class Meta:
        strict = True


class EventSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    owner = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(missing="")
    categories = fields.List(fields.Str, missing=[])
    start_date = fields.DateTime(required=True, format=constants.EVENT_DATE_FORMAT)
    end_date = fields.DateTime(required=True, format=constants.EVENT_DATE_FORMAT)
    start_time = fields.DateTime(required=True, format=constants.EVENT_TIME_FORMAT)
    end_time = fields.DateTime(required=True, format=constants.EVENT_TIME_FORMAT)
    end_date_no_recur = fields.DateTime(required=True, format=constants.EVENT_DATE_FORMAT)

    class Meta:
        strict = True


class EventListSchema(EventSchema):
    occurrence_num = fields.Int(dump_only=True)

    class Meta:
        strict = True


class EventDetailsSchema(EventSchema):
    is_recurring = fields.Bool(missing=False)
    recurrence_details = fields.Nested(RecurrenceDetails, required=False)
    timezone = fields.Str(dump_only=True)

    class Meta:
        strict = True


class EventOccurrenceDetailsSchema(EventDetailsSchema):
    occurrence_num = fields.Int(dump_only=True)

    class Meta:
        strict = True


class EventUpdateSchema(ma.Schema):
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    categories = fields.List(fields.Str, missing=[])
    start_date = fields.DateTime(format=constants.EVENT_DATE_FORMAT)
    end_date = fields.DateTime(format=constants.EVENT_DATE_FORMAT)
    start_time = fields.DateTime(format=constants.EVENT_TIME_FORMAT)
    end_time = fields.DateTime(format=constants.EVENT_TIME_FORMAT)
    end_date_no_recur = fields.DateTime(required=True, format=constants.EVENT_DATE_FORMAT)
    is_recurring = fields.Bool()
    recurrence_details = fields.Nested(RecurrenceDetails)

    class Meta:
        strict = True


class UpdateDetails(ma.Schema):
    update_type = fields.Str(required=True, validate=validate_update_type)
    occurrence_num = fields.Int(missing=1)

    class Meta:
        strict = True


class EventOccurrenceUpdateSchema(ma.Schema):
    update_details = fields.Nested(UpdateDetails, required=True)
    # name = fields.Str(required=True)
    # description = fields.Str(missing="")
    # categories = fields.List(fields.Str, missing=[])
    # start_date = fields.DateTime(required=True, format=constants.EVENT_DATE_FORMAT)
    # end_date = fields.DateTime(required=True, format=constants.EVENT_DATE_FORMAT)
    # start_time = fields.DateTime(required=True, format=constants.EVENT_TIME_FORMAT)
    # end_time = fields.DateTime(required=True, format=constants.EVENT_TIME_FORMAT)
    # is_recurring = fields.Bool()
    # recurrence_details = fields.Nested(RecurrenceDetails)

    class Meta:
        strict = True


class EventFiltersSchema(ma.Schema):
    start_date = fields.DateTime(required=False, missing=None, format=constants.EVENT_DATE_FORMAT)
    end_date = fields.DateTime(required=False, missing=None, format=constants.EVENT_DATE_FORMAT)
    categories = fields.Str(required=False, missing=None)

    class Meta:
        strict = True


class EventDetailsFilterSchema(ma.Schema):
    occurrence_num = fields.Int(missing=1)

    class Meta:
        strict = True


event_list_schema = EventListSchema()
event_details_schema = EventDetailsSchema()
event_details_filter_schema = EventDetailsFilterSchema()
event_filters_schema = EventFiltersSchema()
event_occurrence_details_schema = EventOccurrenceDetailsSchema()
event_occurrence_update_schema = EventOccurrenceUpdateSchema()
event_update_schema = EventUpdateSchema()

