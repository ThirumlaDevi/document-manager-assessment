from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    orgId = serializers.IntegerField()
    userId = serializers.IntegerField()
    chunkId = serializers.CharField(required=False)
