# ML Full-Stack challenge
Your objective is to build an application that lets users apply different filters in a video. The
user should be able to select a video from the computer files, and with the video loaded,
change the filter values and reproduce the video to preview the changes. The filters are up to
you, it could be changing the brightness, saturation, hue, and more - feel free to choose and
be creative. Once satisfied with the changes, the user can export the video to a new file.
So, the application must be able to:
1. Load a video from your computer
2. Choose and apply filters in the video
3. Preview the changes made on video
4. Save the video with the filter applied

Here is a simple example of what the application could look like, but again, feel comfortable
making any changes and use all of your creativity.


![ui example](./docs/imgs/ui.png "Example UI")



You can develop in any programming language, Python is more preferable.
How should you write your code?
- We prefer working on a fresh git repository
- Create objects and functions when possible
- Add comments to your code so we can better assess your thought process
Your solution will be evaluated according to efficiency, functionality, and code readability.

### Requirements
- Docker;
- docker-compose;
- make.

### Install
    make build
    make up
Go to http://0.0.0.0:8000

### Test
    make test


### Improvements:
Videos are currently being encoded using the mp4v format, which causes compatibility issues when viewed in a browser. To fix this issue, the videos are being re-encoded in the h264 format. However, this process takes additional time and can result in a loss of image quality.

There are two potential solutions to this issue:

1. Transforming the video into a series of images, then reconstructing it using FFmpeg while bypassing the VideoWriter function in OpenCV.
2. Installing OpenCV and OpenH264 using conda, but this would require updating the project docker configuration and managing its dependencies.

### Todo:
- sepia filter;
- hue filter;
- improving assertions in tests.
