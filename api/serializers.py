from rest_framework import serializers
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PrimaryKeyNestedMixin(serializers.RelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid pk "{pk_value}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected pk value, received {data_type}.'),
    }

    def __init__(self, **kwargs):
        self.pk_field = kwargs.pop('pk_field', None)
        self.serializer = kwargs.pop('serializer', None)
        super(PrimaryKeyNestedMixin, self).__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(pk=data)
        except models.ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        return self.serializer(value).data
