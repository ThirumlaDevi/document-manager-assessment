from rest_framework import serializers

from file_versions.models import File

class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
