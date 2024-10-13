# Macroblocking Artifact Generator

This project generates synthetic macroblocking artifacts in video frames, simulating real-world encoding errors. The generated artifacts can be used for training and testing models that detect and correct these errors in video processing pipelines.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installing Dependencies](#installing-dependencies)
- [Usage](#usage)
  - [Frame Extraction](#frame-extraction)
  - [Generating Macroblocking Artifacts](#generating-macroblocking-artifacts)
  - [Repackaging the Video](#repackaging-the-video)
- [Example](#example)
- [Customization](#customization)
  - [Directional Shifting](#directional-shifting)
  - [Padding and Blending](#padding-and-blending)
- [Contributing](#contributing)
- [Preliminary Dataset](https://drive.google.com/drive/folders/1z07YbYSiEItlqbWrAN3rdQ76Z6Z8SeWK?usp=sharing)

## Overview
Macroblocking artifacts occur in video frames as a result of compression errors, where parts of an image block are visually corrupted. These artifacts are common in low-bandwidth video streaming and can degrade the user experience. This project allows you to simulate such artifacts by copying pixels, applying random directional shifts, and blending parts of video frames to mimic these issues.

## Features
- **Checkered Pattern Artifacts**: Generates checkered patterns in either half of the image, copying pixels from corresponding halves and applying shifts.
- **Directional Pixel Shifting**: Shifts pixels within blocks in user-defined directions ('up', 'down', 'left', 'right').
- **Padding and Blending**: Optionally apply padding around blocks before copying and blend blocks with the original image for a more natural look.
- **Frame-by-Frame Processing**: Process videos frame-by-frame and repackage them with the injected artifacts.

## Installation

### Prerequisites
- Python 3.x
- OpenCV
- Numpy

### Installing Dependencies
You can install the required Python libraries using pip:

```bash
pip install opencv-python numpy
```

## Usage

### Frame Extraction
Before adding macroblocking artifacts, you'll need to extract frames from the video:

```bash
# Example script for extracting frames using ffmpeg
ffmpeg -i input_video.mp4 frames/frame_%04d.png
```

### Generating Macroblocking Artifacts
Run the script to process the extracted frames and introduce macroblocking artifacts:

```python
from artifact_generator import process_frames_with_middle_copying

# Parameters:
# - Input folder containing frames
# - Output folder for modified frames
# - Block size for checkered pattern
# - Maximum shift value for pixel displacement
# - Padding margin to avoid edge copying
# - Blending factor for smooth block transitions
# - Whether to apply artifacts horizontally or vertically
# - Direction of pixel shifts within blocks ('up', 'down', 'left', 'right')

process_frames_with_middle_copying(
    input_folder='frames',
    output_folder='modified_frames',
    block_size=30,
    max_shift_value=15,
    padding_margin=50,
    blend_factor=0.4,
    horizontal=True,
    direction='left'  # 'left', 'right', 'up', 'down'
)
```

### Repackaging the Video
Once the frames have been processed, you can repackage them into a video:

```bash
# Example script for repackaging frames using ffmpeg
ffmpeg -r 30 -i modified_frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p output_video_with_artifacts.mp4
```

## Example
Here’s an example of generating artifacts in one of the video frames:

Credits- https://www.youtube.com/watch?v=IUN664s7N-c

**Original Image:**

![Original Image -1](https://github.com/user-attachments/assets/1264402a-57a1-41e4-91c6-320f90d5dc8b)
![Original Image -2](https://github.com/user-attachments/assets/bfd4f177-0064-4cff-bfa5-fd8ebe5f5883)


**With Macroblocking Artifacts:**

![With Macroblocking Artifacts-1](https://github.com/user-attachments/assets/14bf03ca-d599-41b9-9b09-02a4272d48a8)
![With Macroblocking Artifacts-2](https://github.com/user-attachments/assets/134be8a7-fe9d-4e1f-9573-5daa744ed293)


## Customization
### Directional Shifting
You can customize the direction of pixel shifts within the blocks. Available directions are:
- up
- down
- left
- right

These directional shifts can simulate different kinds of macroblocking effects.

### Padding and Blending
To avoid copying pixels from the image background (such as white or black areas), you can specify a `padding_margin` to only copy pixels from the middle part of the image. The blocks can also be smoothly blended with the surrounding areas using the `blend_factor` parameter, creating a more natural-looking artifact.


## Contributing
Contributions are welcome! If you'd like to improve this project, feel free to submit a pull request or file an issue.

### How to Contribute:
1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add a new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.


