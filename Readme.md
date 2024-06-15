# Timer Video Generator API
This Flask application provides an API endpoint to generate timer videos with customizable duration, resolution, and output format (MP4 or AVI). It can also be run as a command-line tool to generate videos directly.

## Requirements
- Python 3.x
- Flask
- OpenCV (opencv-python-headless)
- PIL (Pillow)

Install dependencies using pip:

```
pip install Flask opencv-python-headless Pillow
```

## Usage
### Command-Line Tool
Run the script timer_video_generator.py with command-line arguments to generate a timer video:

```
python timer_video_generator.py [duration] [width] [height] --format [mp4/avi]
```

## Arguments:

- duration: Duration of the video in seconds (default: 60.0)
- width: Width of the video resolution (default: 1920)
- height: Height of the video resolution (default: 1080)
- --format: Output file format (MP4 or AVI, default: mp4)

## Example:
```
python timer_video_generator.py 60 1920 1080 --format mp4
```

## API Server
Start the Flask server to run the API:
```
python timer_video_generator.py --api
```

The server will start locally on http://localhost:5000.

## Generate Timer Video Endpoint
Endpoint: /generate

Method: POST

Headers: Content-Type: application/json

Payload:

{
  "duration": 60,
  "width": 1920,
  "height": 1080,
  "format": "mp4"
}

Parameters:

- duration: Duration of the video in seconds.
- width: Width of the video resolution.
- height: Height of the video resolution.
- format: (Optional) Output file format (MP4 or AVI, default: mp4).

## Example API Request

```
wget --post-data='{"duration": 60, "width": 1920, "height": 1080, "format": "mp4"}' \
  --header="Content-Type: application/json" \
  http://localhost:5000/generate -O time_60.mp4
```

This command sends a POST request to generate a timer video with a duration of 60 seconds, resolution 1920x1080, and save it as time_60.mp4.

### Response
The API responds with the generated video file in the specified format (MP4 or AVI).

## Notes
Ensure the required fonts are available on your system for text rendering.
Adjust paths and configurations as per your environment setup.
This application allows you to easily create timer videos either via command-line interface or through a RESTful API, providing flexibility and customization options for your video generation needs.

## Supported Video Formats
By default, OpenCV on most systems supports writing to several popular video formats, including but not limited to:

- MP4 (mp4v codec): MPEG-4 Part 14, widely used for video distribution.
- AVI (XVID codec): Audio Video Interleave, another common format for video storage.
- MKV (X264 codec): Matroska Multimedia Container with H.264 video codec.
- WMV (WMV1 codec): Windows Media Video format.
- FLV (FLV1 codec): Flash Video format, commonly used for web video.

These codecs (mp4v, XVID, X264, WMV1, FLV1, etc.) are provided by the underlying system's video encoding libraries. The script uses cv2.VideoWriter_fourcc function to specify the codec when writing the video file. For example:

- cv2.VideoWriter_fourcc(*'mp4v') for MP4 format.
- cv2.VideoWriter_fourcc(*'XVID') for AVI format.

If you encounter issues with specific formats not being supported, it may be due to the availability of codecs on your system or specific configurations of OpenCV during installation. Ensure your OpenCV installation includes support for the desired codecs by checking the build options or documentation specific to your environment.

In summary, the script as modified should be capable of generating video files in common formats supported by OpenCV, provided that the necessary codecs are available on your system. Adjust the cv2.VideoWriter_fourcc codec identifier accordingly to match your desired output format.

## Author
Prince Jose
prince11jose@hotmail.com
[GitHub](https://github.com/prince11jose)
[LinkedIn](https://www.linkedin.com/in/princejose-devops/)
