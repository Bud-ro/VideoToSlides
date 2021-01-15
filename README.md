# VideoToSlides
A quick python script which attempts to extract the slides from a video. This was made primarily because of professors who don't post slides for their lectures, yet just read directly from them in their lecture.

# Usage:
usage: video_to_slide.py [-h] filename [--speed] [--threshold]

positional arguments:
  filename     Name of the video file to convert.
  --speed      Number of seconds between frames read. Default is 2.
  --threshold  Percent difference needed to detect a frame change. Default of 5 percent.

optional arguments:
  -h, --help   show this help message and exit
