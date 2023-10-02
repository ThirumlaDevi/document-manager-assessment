from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from uploader.serializers import FileUploadSerializer
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import renderer_classes
import logging
import psycopg2
import time

logger = logging.getLogger("mylogger")

@csrf_exempt #need to find a better way to hit post with csrf tokens
# recommondations didn't work https://stackoverflow.com/questions/10628275/how-to-use-curl-with-django-csrf-tokens-and-post-requests
# @api_view(['POST']) # throws authentication credentials not provided error
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def uploadChunk(request):
    # Reference to convert bytes to json https://stackoverflow.com/questions/40059654/convert-a-bytes-array-into-json-format
    serializer = FileUploadSerializer(data=json.loads(request.headers['Details']))
    # ultimately move the user information to bearer token and name the file as chunk id

    if serializer.is_valid():
        # serializer.save()
        # push request.FILES['chunk'] along with other information to blob storage
        isTransactionSuccessful = updateDB(serializer.data, request.FILES['chunk'])
        if isTransactionSuccessful == None:
            logger.info("file chunk upload to DB was successful")
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.info("file chunk upload to DB was not successful")
            return JsonResponse({"error": "file chunk upload to DB was not successful"}, status=status.HTTP_502_BAD_GATEWAY)
    logger.info("file chunk upload failed user or file details missing in the header")
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def updateDB(chunkDetails, chunk):
    # Connect to the PostgreSQL database
    # For now hardcoding the db and connection information
    conn = psycopg2.connect(database="chunk_data", user="dev",
                            password="localDevPassword", host="localhost")
    
    # Open a cursor to perform database operations
    cur = conn.cursor()
    isTransactionSuccessful = False
    # make the transaction and rollback on failure
    # with conn.transaction():
    isTransactionSuccessful = cur.execute("INSERT INTO chunks VALUES (%s, %s, %s, %s, %s)", 
                     (chunkDetails['orgId'],chunkDetails['userId'],chunkDetails['chunkId'],
                      time.time(), chunk.file.read()))
        # need to figure out a better way to produce epoc time

    conn.commit()

    # everytime request is made connection is opened and close, 
    # Need to change it as when application shuts down close the communication with database
    cur.close()
    conn.close()
    return isTransactionSuccessful

@csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def other(request):
    return {}