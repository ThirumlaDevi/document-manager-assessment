from rest_framework import serializers
import uploader.customFields.chunk as ChunkField

class FileUploadSerializer(serializers.Serializer):
    orgId = serializers.IntegerField()
    userId = serializers.IntegerField()
    chunkId = serializers.CharField()
