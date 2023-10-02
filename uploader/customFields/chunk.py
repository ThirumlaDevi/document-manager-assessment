from rest_framework import serializers

# this was we can reuse the fields for serialising other requests that might send these in their body
# reference -> https://medium.com/@luccascorrea/django-rest-framework-creating-a-custom-serializer-field-de3e29846bc
class ChunkField(serializers.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return data