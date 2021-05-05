from django.urls import path, include

from .models import Song, Podcast, AudioBook
from . import views

urlpatterns = [
    path('<audioFileType>/<audioFileID>', views.RetrieveUpdateDeleteAudioFileView.as_view()),
    path('<audioFileType>/', views.RetrieveAudioFileView.as_view()),
    path('audiofiles/', views.AudioFileView.as_view()),

]