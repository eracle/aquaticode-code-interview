from django import forms
from django.forms import FileInput

from .models import Video


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["video_file"]
        widgets = {
            "video_file": FileInput(
                attrs={
                    "accept": "video/*",
                    "class": "form-control",
                }
            ),
        }


class VideoFiltersForm(forms.Form):
    brightness = forms.IntegerField(
        min_value=-100,
        max_value=100,
        initial=0,
        widget=forms.NumberInput(attrs={"type": "range", "min": -100, "max": 100}),
    )
    saturation = forms.IntegerField(
        min_value=-100,
        max_value=100,
        initial=0,
        widget=forms.NumberInput(attrs={"type": "range", "min": -100, "max": 100}),
    )
    blur = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=0,
        widget=forms.NumberInput(attrs={"type": "range", "min": 0, "max": 100}),
    )
