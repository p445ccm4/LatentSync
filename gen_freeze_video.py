import cv2
import numpy as np
import argparse

# Parameters
# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate a video from a single image.')
parser.add_argument('image_path', type=str, help='Path to the input image')
parser.add_argument('output_video_path', type=str, help='Path to the output video')
parser.add_argument('video_length', type=int, help='Length of the video in seconds')
args = parser.parse_args()

image_path = args.image_path
output_video_path = args.output_video_path
video_length = args.video_length
frame_rate = 15
# frame_size = (640, 480)  # Width, Height
frame_count = video_length * frame_rate

# Load the image
image = cv2.imread(image_path)
if image is None:
    raise ValueError("Image not found or unable to load.")

# Resize the image to fit within 640x480 while maintaining aspect ratio
height, width = image.shape[:2]
desired_height, desired_width = 480, 640
aspect_ratio = width / height

if aspect_ratio > desired_width / desired_height:
    new_width = desired_width
    new_height = int(new_width / aspect_ratio)
else:
    new_height = desired_height
    new_width = int(new_height * aspect_ratio)

image = cv2.resize(image, (new_width, new_height))

# Pad the image to 640x480
height, width = image.shape[:2]
top = (desired_height - height) // 2
bottom = desired_height - height - top
left = (desired_width - width) // 2
right = desired_width - width - left
image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
height, width = image.shape[:2]

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

# Write the same frame multiple times
for _ in range(frame_count):
    out.write(image)

# Release everything if job is finished
out.release()