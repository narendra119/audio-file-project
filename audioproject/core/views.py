from django.shortcuts import render

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

from .models import Song, Podcast, AudioBook
from .serializers import CreateSongSerializer, CreatePodcastSerializer, CreateAudioBookSerializer

import datetime
# Create your views here.

class AudioFileView(GenericAPIView):
    
    def get_serializer_class(self, audioFileType):
        if audioFileType == "song":
            return CreateSongSerializer
    
        if audioFileType == "podcast":
            return CreatePodcastSerializer
    
        if audioFileType == "audiobook":
            return CreateAudioBookSerializer
    
    def post(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        response = {}
        request_data = request.data
        audioFileType = request_data.get('audioFileType')
        audioFileMetadata = request_data.get('audioFileMetadata')
        audioFileMetadata['uploaded_time'] = datetime.datetime.now()

        serializer = self.get_serializer_class(audioFileType)
        serializer_data = serializer(data = audioFileMetadata)
        is_validated_data = serializer_data.is_valid()

        if is_validated_data:
            if audioFileType == 'song':
                instance = Song.objects.create(**serializer_data.validated_data)
                instance.save()
                response["msg"] = "Data Saved Successfully"
                status_code = status.HTTP_200_OK

            elif audioFileType == 'podcast':
                instance = Podcast.objects.create(**serializer_data.validated_data)
                instance.save()
                response["msg"] = "Data Saved Successfully"
                status_code = status.HTTP_200_OK

            elif audioFileType == 'audiobook':
                instance = AudioBook.objects.create(**serializer_data.validated_data)
                instance.save()
                response["msg"] = "Data Saved Successfully"
                status_code = status.HTTP_200_OK
        else:
            response["errors"] = serializer_data.errors
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response, status=status_code)
        
class RetrieveUpdateDeleteAudioFileView(GenericAPIView):

    def get_serializer(self, audioFileType=None):
        if audioFileType == "audiobook":
            return CreateAudioBookSerializer

        if audioFileType == "song":
            return CreateSongSerializer

        if audioFileType == "podcast":
            return CreatePodcastSerializer

    def get(self, request, audioFileType, audioFileID, *args, **kwargs):
        audioFileType = audioFileType
        serializer_class = self.get_serializer(audioFileType=audioFileType)

        response = {}
        
        if audioFileType == "song":
            try:
                dct = {}
                instance = Song.objects.get(id=audioFileID)
                dct['name'] = instance.name
                dct['duration'] = instance.duration
                dct['uploaded_time'] = instance.uploaded_time
                # data = SongSerializer(instance)
                response['msg'] = "Data Fetched Successfully"
                response['filetype'] = "song"
                response['data'] = dct
                status_code = status.HTTP_200_OK
            except Song.DoesNotExist:
                response['msg'] = f"Song with id {audioFileID} Does not exist"
                status_code = status.HTTP_400_BAD_REQUEST

        elif audioFileType == "podcast":
            try:
                data = {}
                instance = Podcast.objects.get(id=audioFileID)

                data['name'] = instance.name
                data['duration'] = instance.duration
                data['uploaded_time'] = instance.uploaded_time
                data['host'] = instance.host
                data['participants'] = instance.participants

                response['msg'] = "Data Fetched Successfully"
                response['filetype'] = "podcast"
                response['data'] = data
                status_code = status.HTTP_200_OK
            except Podcast.DoesNotExist:
                response['msg'] = f"Podcast with id {audioFileID} Does not exist"
                status_code = status.HTTP_400_BAD_REQUEST


        elif audioFileType == "audiobook":
            try:
                data = {}
                instance = AudioBook.objects.get(id=audioFileID)

                data['title'] = instance.title
                data['author'] = instance.author
                data['narrator'] = instance.narrator
                data['duration'] = instance.duration
                data['uploaded_time'] = instance.uploaded_time

                response['msg'] = "Data Fetched Successfully"
                response['filetype'] = "audiobook"
                response['data'] = data
                status_code = status.HTTP_200_OK
            except Podcast.DoesNotExist:
                response['msg'] = f"Podcast with id {audioFileID} Does not exist"
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            response['msg'] = "Invalid input, please check"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)
        

    def put(self, request, audioFileType, audioFileID, *args, **kwargs):
        response = {}

        if audioFileType == "song":
            try:
                instance = Song.objects.get(id=audioFileID)
                serialized_data = SongSerializer(instance)
                is_validated_data = serialized_data.is_valid()
                
                if is_validated_data:
                    name = serialized_data.validated_data.get("name")
                    duration = serialized_data.validated_data.get("duration")

                    instance.name = name
                    instance.duration = duration
                    instance.uploaded_time = datetime.datetime.now()

                    instance.save()
                    response['msg'] =  "Song Details Updated Successfully"
                    status_code = status.HTTP_200_OK
                else:
                    response['msg'] =  serialized_data.errors
                    status_code = status.HTTP_400_BAD_REQUEST

            except Song.DoesNotExist:
                response['msg'] = f"Song with id {audioFileID} Does not exist"
                status_code = status.HTTP_400_BAD_REQUEST

        elif audioFileType == "podcast":

            try:
                instance = Podcast.objects.get(id=audioFileID)
                serialized_data = PodcastSerializer(instance)
                is_validated_data = serialized_data.is_valid()
                
                if is_validated_data:
                    name = serialized_data.validated_data.get("name")
                    duration = serialized_data.validated_data.get("duration")
                    host = serialized_data.validated_data.get("host")

                    instance.name = name
                    instance.duration = duration
                    instance.host = host
                    instance.uploaded_time = datetime.datetime.now()

                    instance.save()
                    response['msg'] =  "Song Details Updated Successfully"
                    status_code = status.HTTP_200_OK
                else:
                    response['msg'] =  serialized_data.errors
                    status_code = status.HTTP_400_BAD_REQUEST

            except Podcast.DoesNotExist:
                response['msg'] = f"Podcast with id {audioFileID} Does not exist"
                status_code = status.HTTP_400_BAD_REQUEST
         
        elif audioFileType == "audiobook":
            try:
                instance = AudioBook.objects.get(id=audioFileID)
                serialized_data = AudioBookSerializer(instance)
                is_validated_data = serialized_data.is_valid()
                
                if is_validated_data:
                    name = serialized_data.validated_data.get("name")
                    duration = serialized_data.validated_data.get("duration")
                    host = serialized_data.validated_data.get("host")

                    instance.name = name
                    instance.author = author
                    instance.narrator = narrator
                    instance.duration = duration
                    instance.uploaded_time = datetime.datetime.now()

                    instance.save()
                    response['msg'] =  "Song Details Updated Successfully"
                    status_code = status.HTTP_200_OK
                else:
                    response['msg'] =  serialized_data.errors
                    status_code = status.HTTP_400_BAD_REQUEST
            except AudioBook.DoesNotExist:
                response['msg'] = f"AudioBook with id {audioFileID} Does not exist"
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            response['msg'] = "Invalid input, please check"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)


    def delete(self, request, audioFileType, audioFileID, *args, **kwargs):
        response = {}

        if audioFileType == "song":
            try:
                instance = Song.objects.get(id=audioFileID)
                instance.delete()
                response['msg'] = "Song Deleted Successfully"
                status_code = status.HTTP_200_OK
            except Song.DoesNotExist:
                response['msg'] = "Song Does not exist"
                status_code = status.HTTP_400_BAD_REQUEST

        elif audioFileType == "podcast":
            try:
                instance = Podcast.objects.get(id=audioFileID)
                instance.delete()
                response['msg'] = "Podcast Deleted Successfully"
                status_code = status.HTTP_200_OK
            except Podcast.DoesNotExist:
                response['msg'] = "Podcast Does not exist"
                status_code = status.HTTP_400_BAD_REQUEST
         
        elif audioFileType == "audiobook":
            try:
                instance = AudioBook.objects.get(id=audioFileID)
                instance.delete()
                response['msg'] = "AudioBook Deleted Successfully"
                status_code = status.HTTP_200_OK
            except AudioBook.DoesNotExist:
                response['msg'] = "AudioBook Does not exist"
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            response['msg'] = "Invalid input, please check"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)

class RetrieveAudioFileView(GenericAPIView):

    def get(self, request, audioFileType, *args, **kwargs):
        response = {}

        if audioFileType == "song":
            all_data = Song.objects.all()
            count = all_data.count()

            result = []
            for obj in all_data:
                data = {}
                data['name'] = obj.name
                data['duration'] =obj.duration
                data['host'] = obj.host
                data['uploaded_time'] = obj.uploaded_time
                result.append(data)

            response['msg'] = "Data Fetched Successfully"
            response['data'] = result
            response['count'] = count
            status_code = status.HTTP_200_OK

        elif audioFileType == "podcast":
            all_data = Podcast.objects.all()
            count = all_data.count()
            data = PodcastSerializer(all_data, many = True)

            response['msg'] = "Data Fetched Successfully"
            response['data'] = data
            response['count'] = count
            status_code = status.HTTP_200_OK
         
        elif audioFileType == "audiobook":
            all_data = AudioBook.objects.all()
            count = all_data.count()
            data = AudioBookSerializer(all_data, many = True)

            response['msg'] = "Data Fetched Successfully"
            response['data'] = data
            response['count'] = count
            status_code = status.HTTP_200_OK
        else:
            response['msg'] = "Invalid input, please check"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)