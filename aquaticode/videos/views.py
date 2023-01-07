from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponseServerError
from django.shortcuts import redirect, render
from django.views.generic import DetailView

from .forms import VideoFiltersForm, VideoUploadForm
from .models import Video
from .utils import apply_filters


def landing_page(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            return redirect("video-detail", pk=video.id)
    else:
        form = VideoUploadForm()
    return render(request, "videos/landing_page.html", {"form": form})


class DetailVideoView(DetailView):
    model = Video

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = VideoUploadForm()
        context["filters_form"] = VideoFiltersForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = VideoFiltersForm(request.POST)
        if not form.is_valid():
            raise ValidationError("Filters not valid.")
        else:
            brightness = form.cleaned_data["brightness"]
            saturation = form.cleaned_data["saturation"]
            blur = form.cleaned_data["blur"]

            # Apply the filters to the video using the provided parameters
            file_content = apply_filters(
                video_path=self.object.video_file.path,
                brightness=brightness,
                saturation=saturation,
                blur=blur,
            )
            if not file_content:
                return HttpResponseServerError("Error encoding the video")

            with transaction.atomic():
                self.object.video_file.delete()
                self.object.video_file.save(name="video.mp4", content=ContentFile(file_content))

            context = self.get_context_data(object=self.object)
            context["filters_form"] = form
            return render(request, "videos/video_detail.html", context)


video_detail = DetailVideoView.as_view()
