"""
Title: Timer Video Generator

Author: Prince Jose
Email: prince11jose@hotmail.com
Date Created: 2024-06-15
Last Modified: 2024-06-15
Description: This script generates a video displaying a countdown timer. It can be run as a standalone script or as a Flask API service.

Usage:
    As a standalone script:
        python timer_video_generator.py [duration] [width] [height] --format [mp4|avi]

    As an API:
        python timer_video_generator.py --api

    As an API in production:
        python timer_video_generator.py --api --prod

Dependencies:
    - argparse
    - cv2 (OpenCV)
    - numpy
    - Flask
    - PIL (Pillow)

License: MIT License
"""

import argparse
import cv2
import numpy as np
from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import os
import sys

app = Flask(__name__)

def make_frame(t, duration, resolution, font):
    # Create an empty white image
    frame = np.ones((resolution[1], resolution[0], 3), dtype=np.uint8) * 255

    # Calculate remaining time
    remaining_time = duration - t
    hours = int(remaining_time // 3600)
    minutes = int((remaining_time % 3600) // 60)
    seconds = int(remaining_time % 60)
    
    # Format the time as HH:MM:SS
    text = f"{hours:02}:{minutes:02}:{seconds:02}"

    # Convert to PIL Image to draw text
    pil_image = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_image)

    # Define the text and its position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
    text_x = (resolution[0] - text_size[0]) // 2
    text_y = (resolution[1] - text_size[1]) // 2

    # Draw the text on the image
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    # Convert back to numpy array
    frame = np.array(pil_image)

    return frame

def generate_video(duration, width, height, output_filename, file_format):
    supported_formats = {
        'mp4': {'codec': 'mp4v'},
        'avi': {'codec': 'XVID'},
        'mkv': {'codec': 'XVID'},
        'wmv': {'codec': 'XVID'},
    }

    # Check if the specified format is supported
    if file_format not in supported_formats:
        raise ValueError(f"Unsupported file format '{file_format}'. Supported formats are: {', '.join(supported_formats.keys())}")
    
    resolution = (width, height)
    fps = 24
    num_frames = int(duration * fps)

    # Load a font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 70)

    # Define the codec and create VideoWriter object
    output_path = f"{output_filename}.{file_format}"
    fourcc = cv2.VideoWriter_fourcc(*supported_formats[file_format]['codec'])
    out = cv2.VideoWriter(output_path, fourcc, fps, resolution)

    for i in range(num_frames):
        t = i / fps
        frame = make_frame(t, duration, resolution, font)
        out.write(frame)

    # Release everything when done
    out.release()

    return output_path

@app.route('/generate', methods=['POST'])
def generate_timer_video():
    data = request.json
    duration = data.get('duration')
    width = data.get('width')
    height = data.get('height')
    file_format = data.get('format', 'mp4')  # Default to mp4 if format is not provided

    if not all([duration, width, height]):
        return jsonify({"error": "Please provide duration, width, and height"}), 400

    output_filename = f"time_{int(duration)}"
    try:
        output_path = generate_video(duration, width, height, output_filename, file_format)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return send_file(output_path, as_attachment=True, download_name=f"{output_filename}.{file_format}")

def main():
    parser = argparse.ArgumentParser(description="Generate a video with running time text.")
    parser.add_argument("duration", type=float, nargs='?', default=60.0, help="Duration of the video in seconds (default: 60.0)")
    parser.add_argument("width", type=int, nargs='?', default=1920, help="Width of the video resolution (default: 1920)")
    parser.add_argument("height", type=int, nargs='?', default=1080, help="Height of the video resolution (default: 1080)")
    parser.add_argument("--format", type=str, default="mp4", choices=["mp4", "avi", "mkv", "wmv", "flv"], help="Output file format")
    parser.add_argument("--api", action="store_true", help="Run as API service")
    parser.add_argument("--prod", action="store_true", help="Run in production mode")

    args = parser.parse_args()

    if args.api:
        if args.prod:
            from gunicorn.app.base import BaseApplication

            class StandaloneApplication(BaseApplication):
                def __init__(self, app, options=None):
                    self.options = options or {}
                    self.application = app
                    super().__init__()

                def load_config(self):
                    config = {key: value for key, value in self.options.items()
                              if key in self.cfg.settings and value is not None}
                    for key, value in config.items():
                        self.cfg.set(key.lower(), value)

                def load(self):
                    return self.application

            options = {
                'bind': '0.0.0.0:8000',
                'workers': 4,
            }
            StandaloneApplication(app, options).run()
        else:
            app.run(debug=True, host='0.0.0.0')
    else:
        output_filename = f"time_{int(args.duration)}"
        output_path = generate_video(args.duration, args.width, args.height, output_filename, args.format)
        print(f"Video saved as {output_path}")

if __name__ == "__main__":
    main()
