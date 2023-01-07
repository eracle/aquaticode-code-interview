import os
import shutil
import subprocess
import uuid

import cv2
import numpy as np
from PIL import Image, ImageEnhance


def apply_filters(video_path, brightness, saturation, blur):
    # Create a temporary directory to store the images
    temp_dir = "/tmp/{}".format(uuid.uuid4())
    os.makedirs(temp_dir)

    # Use OpenCV to split the video into images
    video = cv2.VideoCapture(video_path)

    i = 0
    # Process each frame of the input video
    while video.isOpened():
        # Read a frame from the input video
        ret, frame = video.read()

        # If the frame is empty, break the loop
        if frame is None:
            break

        # Apply the filters to the frame
        frame = process_frame(frame, brightness, saturation, blur)

        cv2.imwrite(os.path.join(temp_dir, "{:05d}.jpg".format(i)), frame)
        i += 1

    # Get the Frames per Second
    fps = video.get(cv2.CAP_PROP_FPS)

    # Release the video file handle
    video.release()

    # Generate random output file name
    filename = str(uuid.uuid4())
    output_file_name = f"{filename}.mkv"

    # Use ffmpeg to rebuild the video from the images
    subprocess.run(
        [
            "ffmpeg",
            "-r",
            str(fps),
            "-i",
            os.path.join(temp_dir, "%05d.jpg"),
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-qp",
            "0",
            output_file_name,
        ]
    )

    # Clean up by deleting the temporary directory
    shutil.rmtree(temp_dir)

    # Get file content
    with open(output_file_name, mode="rb") as file:
        file_content = file.read()

    # Delete file
    os.remove(output_file_name)

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
