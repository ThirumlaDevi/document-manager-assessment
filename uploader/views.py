import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from uploader.serializers import FileUploadSerializer
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import renderer_classes
from django.http import HttpResponse
import logging
import psycopg2
import time
import base64

logger = logging.getLogger("mylogger")

@csrf_exempt #need to find a better way to hit post with csrf tokens
# recommondations didn't work https://stackoverflow.com/questions/10628275/how-to-use-curl-with-django-csrf-tokens-and-post-requests
# @api_view(['POST']) # throws authentication credentials not provided error
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def uploadChunk(request):
    # Reference to convert bytes to json https://stackoverflow.com/questions/40059654/convert-a-bytes-array-into-json-format
    serializer = FileUploadSerializer(data=json.loads(request.headers['details']))
    # ultimately move the user information to bearer token and name the file as chunk id
    if serializer.is_valid():
        # push request.FILES['chunk'] along with other information to blob storage
        isTransactionSuccessful = updateDB(serializer.data, request.FILES['chunk'])
        if isTransactionSuccessful == None:
            logger.info("file chunk upload to DB was successful")
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.info("file chunk upload to DB was not successful")
            return HttpResponse({"error": "file chunk upload to DB was not successful"}, status=status.HTTP_502_BAD_GATEWAY)
    logger.info("file chunk upload failed user or file details missing in the header")
    # For some reason react looks for only HttpResponses and no generic Json response
    return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        #Todo - need to figure out a better way to produce epoc time

    conn.commit()

    # everytime request is made connection is opened and close, 
    # Need to change it as when application shuts down close the communication with database
    cur.close()
    conn.close()
    return isTransactionSuccessful

@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get(request, id):
    serializer = FileUploadSerializer(data=json.loads(request.headers['Details']))
    if serializer.is_valid():
        chunkRecord = getChunkFromDB(serializer.data, id)
        if chunkRecord != None:
            base64_data = base64.b64encode(chunkRecord[0]).decode('utf-8')
            # How to send chunk data to frontend without broken pipe error 
            # reference -> https://stackoverflow.com/a/68455671
            return HttpResponse(base64_data, status=status.HTTP_200_OK) # returns data in base64
    return HttpResponse({"error": "docID is incorrect or user doesn't have read access to chunk"})


def getChunkFromDB(chunkDetails, chunkId):
    # Todo - introduce indices in postgres tables too
    conn = psycopg2.connect(database="chunk_data", user="dev",
                            password="localDevPassword", host="localhost")
    
    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute("select data from chunks where orgId=%s AND userId=%s AND chunkId=%s", 
        (chunkDetails['orgId'],chunkDetails['userId'],chunkId))
    
    chunkRecord = None
    chunkRecord = cur.fetchone()
    # conn.commit()

    # Todo - everytime request is made connection is opened and close, 
    # Need to change it as when application shuts down close the communication with database
    cur.close()
    conn.close()
    return chunkRecord