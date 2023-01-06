import os
import subprocess
import uuid
from os import path

import cv2
import numpy as np
from PIL import Image, ImageEnhance


def apply_filters(video_path, brightness, saturation, blur):
    video = cv2.VideoCapture(video_path)

    # Initialize the output video with the same frame size and fps as the input video
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # Random generated filename
    filename = str(uuid.uuid4())
    output_file_name = f"{filename}.mp4"
    output_video = cv2.VideoWriter(output_file_name, fourcc, fps, (width, height))

    # Process each frame of the input video
    while video.isOpened():
        # Read a frame from the input video
        ret, frame = video.read()

        # If the frame is empty, break the loop
        if frame is None:
            break

        # Apply the filters to the frame
        frame = process_frame(frame, brightness, saturation, blur)

        output_video.write(frame)

    # Release the video file handle
    video.release()
    output_video.release()

    # OpenCV didn't successfully make it
    if not path.exists(output_file_name):
        return None

    # Convert back to h264 encoding
    h264_output_file_name = f"p-{output_file_name}"
    subprocess.call(
        [
            "ffmpeg",
            "-i",
            output_file_name,
            "-c:v",
            "libx264",
            "-crf",
            "20",
            h264_output_file_name,
        ]
    )

    # ffmpeg didn't successfully make it
    if not path.exists(h264_output_file_name):
        # Delete file
        os.remove(output_file_name)
        return None

    # Get file content
    with open(h264_output_file_name, mode="rb") as file:
        file_content = file.read()

    # Delete files
    os.remove(output_file_name)
    os.remove(h264_output_file_name)

    return file_content


def process_frame(frame, brightness, saturation, blur):
    # ## Apply the blur filter
    frame = cv2.GaussianBlur(frame, (5, 5), blur)

    # ##  Convert the image to RGB format
    cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ## Convert the image to a Pillow image
    pil_image = Image.fromarray(cv_image)

    # ## image brightness enhancer
    enhancer = ImageEnhance.Brightness(pil_image)
    pil_image = enhancer.enhance(1.0 + (brightness / 100.0))

    # ## image saturation enhancer
    converter = ImageEnhance.Color(pil_image)
    pil_image = converter.enhance(1.0 + (saturation / 100.0))

    # ## Convert the image to a NumPy array
    np_image = np.array(pil_image)

    # Convert the image to BGR format
    frame = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

    return frame
