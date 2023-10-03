# from django.shortcuts import render

# from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
# from rest_framework.viewsets import GenericViewSet

# from file_versions.models import File
# from .serializers import FileInfoSerializer

# class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
#     authentication_classes = []
#     permission_classes = []
#     serializer_class = FileInfoSerializer
#     queryset = File.objects.all()
#     # lookup_field = "file_version_id"

#     def create():
#         return serializer_class.data
    
#     def list():
#         return {}
    
#     def getByRevision():
#         return {}

from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .serializers import FileInfoSerializer
from rest_framework import status

logger = logging.getLogger("mylogger")

@method_decorator(csrf_exempt, name='dispatch')
class FileInfo(View):
    def get(self, request, *args, **kwargs):
        # get user id , org id 
        request.query_params
        return HttpResponse('This is GET request')
    
    def post(self, request, *args, **kwargs):
        logger.info(request.POST)
        # logger.info(json.dumps(request.POST))
        # serializer = FileInfoSerializer(data=json.dumps(request.POST))
        # if serializer.is_valid():
        #     logger.info("file detail upload to DB was successful")
        #     return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        # return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return {}
    
    def getByRevision(request, versionNumber):
        request.query_params
        return HttpResponse('This is GET by revision number request')
