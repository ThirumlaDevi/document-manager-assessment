from rest_framework import serializers

from file_versions.models import File
from file_versions.models import FileVersionInformation

# Nested serialisers reference --> https://stackoverflow.com/a/75387440
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

class FileInfoSerializer(serializers.ModelSerializer):
    file_version_id = FileSerializer()

    class Meta:
        model = FileVersionInformation
        fields = "__all__"
