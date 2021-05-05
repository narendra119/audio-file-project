from rest_framework import serializers
from .models import Song, Podcast, AudioBook
from django.db.models import Q


class CreateSongSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        max_length=100
    )

    duration = serializers.CharField(
        required=True,
        max_length=100
    )

    uploaded_time = serializers.CharField(
        required=True,
        max_length=100
    )

    @classmethod
    def validate(cls, data):

        errors = {}
        name = data.get("name")
        duration = data.get("duration")
        uploaded_time = data.get("uploaded_time")

        name_query = Q(
            name__iexact=name
        )

        existing_name = Song.objects.filter(
            name_query
        ).exists()

        if existing_name:
            errors["name"] = 'This name already exists.'

        if errors:
            raise serializers.ValidationError(errors)

        return super(CreateSongSerializer, cls).validate(cls, data)


class CreatePodcastSerializer(serializers.Serializer):

    name = serializers.CharField(
        required=True,
        max_length=100
    )

    duration = serializers.CharField(
        required=True,
        max_length=100
    )

    uploaded_time = serializers.CharField(
        required=True,
        max_length=100
    )

    host = serializers.CharField(
        max_length=100
    )
    participants = serializers.CharField()


    @classmethod
    def validate(cls, data):

        errors = {}
        name = data.get("name")
        duration = data.get("duration")
        host = data.get("host")
        participants = data.get("participants")
        uploaded_time = data.get("uploaded_time")


        name_query = Q(
            name__iexact=name
        )

        existing_name = Podcast.objects.filter(
            name_query
        ).exists()

        if existing_name:
            errors["name"] = 'This name already exists.'

        participants = eval(participants)
        if not (participants, list):
            errors['participants'] = 'please send in string list representation'
            
        elif len(participants) > 10:
            errors['participants'] = "cannot have more than 10 participants"

        if errors:
            raise serializers.ValidationError(errors)

        return super(CreatePodcastSerializer, cls).validate(cls, data)


class CreateAudioBookSerializer(serializers.Serializer):

    title = serializers.CharField(
        required=True,
        max_length=100
    )

    author = serializers.CharField(
        required=True,
        max_length=100
    )

    uploaded_time = serializers.CharField(
        required=True,
        max_length=100
    )

    narrator = serializers.CharField(
        max_length=100
    )
    duration = serializers.CharField()

    @classmethod
    def validate(cls, data):

        errors = {}

        title = data.get("title")
        author = data.get("duration")
        narrator = data.get("duration")
        duration = data.get("duration")
        uploaded_time = data.get("uploaded_time")

        name_query = Q(
            title__iexact=title
        )

        existing_name = AudioBook.objects.filter(
            name_query
        ).exists()

        if existing_name:
            errors["title"] = 'This title already exists.'

        if errors:
            raise serializers.ValidationError(errors)

        return super(CreateAudioBookSerializer, cls).validate(cls, data)