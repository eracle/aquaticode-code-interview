from factory.django import DjangoModelFactory, FileField

from aquaticode.videos.models import Video


class VideoFactory(DjangoModelFactory):
    class Meta:
        model = Video

    video_file = FileField(filename="test_video.mp4")
