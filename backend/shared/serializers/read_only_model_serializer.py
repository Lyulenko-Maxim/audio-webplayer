from rest_framework import serializers


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        for field in fields:
            fields[field].read_only = True
        return fields

    def create(self, validated_data):
        raise NotImplementedError('Method not allowed in ReadOnlyModelSerializer')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not allowed in ReadOnlyModelSerializer')
