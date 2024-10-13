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
- [License](#license)

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
