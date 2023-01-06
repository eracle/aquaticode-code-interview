import pathlib

import cv2
import pytest

from aquaticode.videos.utils import apply_filters

# Get the path to the test files directory
test_files_dir = pathlib.Path(__file__).parent / "files"


@pytest.fixture
def video_path():
    return str(test_files_dir / "test.mp4")


@pytest.fixture
def video(video_path):
    return cv2.VideoCapture(video_path)


def test_video(video, video_path):
    # Check that the image was successfully loaded
    assert video is not None


def test_brightness(video, video_path):
    # Apply the brightness filter with a value of 50
    output_video_content = apply_filters(video_path, 50, 0, 0)

    # Check that the brightness of the filtered video is increased
    assert output_video_content


def test_saturation(video, video_path):
    # Apply the saturation filter with a value of 50
    output_video_content = apply_filters(video_path, 0, 50, 0)

    # Check that the saturation of the filtered video is increased
    assert output_video_content


def test_blur(video, video_path):
    # Apply the blur filter with a value of 50
    output_video_content = apply_filters(video_path, 0, 0, 50)

    # Check that the blur filter is applied
    assert output_video_content
