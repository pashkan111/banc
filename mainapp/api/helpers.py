from rest_framework import serializers


class SerializerWriteAllowMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        super().__init__(method_name, **kwargs)
        self.read_only = False

    def to_internal_value(self, data):
        return {self.field_name: data}