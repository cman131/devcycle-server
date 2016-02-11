import logging
from django import forms
from django.core.exceptions import ValidationError
from django.utils.dateformat import DateFormat
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.utils.timezone import get_default_timezone

logger = logging.getLogger(__name__)

class UnixDateTimeField(forms.DateTimeField):
    def to_python(self, value):
        dt = None
        try:
            dt = datetime.strptime(' '.join(value), '%Y-%m-%d %H:%M')
        except ValueError:
            try:
                dt = datetime.strptime(' '.join(value), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValidationError('Please enter a valid DateTime (Y-m-d H:M:S')
        if dt is not None:
            df = DateFormat(dt)
            dt = int(df.U())
        return dt

    def prepare_value(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value, get_default_timezone())
        return value

    def bound_data(self, data, initial):
        if data is not None:
            return parse_datetime(str(data))
        
