from enum import Enum
from typing import Any, Dict, List, Tuple, Type, Union

from django.core import exceptions
from django.db.models import CharField


class DbEnum(Enum):
    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(tag.name, tag.value) for tag in cls]

    @classmethod
    def keys(cls) -> List[Tuple[str]]:
        return [tag.name for tag in cls]

    @classmethod
    def keys_lower(cls) -> List[Tuple[str]]:
        return [tag.name.lower() for tag in cls]

    def __str__(self):
        # Yep, we don't include type name, but django forms will work without any friction
        return self.name


class EnumField(CharField):
    __enum: Type[DbEnum]

    def __init__(self, *args, enum: Union[Type[DbEnum], Dict[str, Any]], **kwargs):
        if isinstance(enum, type):
            self.__enum = enum
        else:
            self.__enum = DbEnum(**enum)
        choices = self.__enum.choices()
        max_length = max(len(val) for (val, _) in choices)
        super().__init__(choices=choices, max_length=max_length, *args, **kwargs)

        # Disable default validator for max length
        self.validators.clear()

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        kwargs['enum'] = {
                'value': self.__enum.__name__,
                'names': {tag.name: tag.value for tag in self.__enum},
        }
        del kwargs['choices']
        del kwargs['max_length']

        return name, path, args, kwargs

    def validate(self, value, model_instance):
        if not isinstance(self.to_python(value), self.__enum):
            raise exceptions.ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': value},
            )

    def from_db_value(self, value, _expression, _connection):
        try:
            return self.__enum[value]
        except KeyError:
            return super().to_python(value)

    def to_python(self, value):
        if isinstance(value, self.__enum):
            return value

        try:
            return self.__enum[value]
        except KeyError:
            return super().to_python(value)

    def get_prep_value(self, value):
        if isinstance(value, self.__enum):
            return value.name
        return super().get_prep_value(value)
