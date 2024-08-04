# Face Comparison and Information Extraction API

This project provides a RESTful API for comparing faces, extracting information from images, and detecting/cropping faces using DeepFace and Google's Gemini AI.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Dependencies](#dependencies)
- [License](#license)

## Overview

This project offers an API to compare faces from two images, extract information from an image, and detect/crop the largest face in an image. It uses DeepFace for face verification, Google's Gemini AI for information extraction, and OpenCV for face detection.

## Features

- Compare two faces to determine if they are the same person.
- Extract information from an image.
- Detect and crop the largest face in an image.

## Setup

### Prerequisites

- Python 3.x
- Flask
- DeepFace
- OpenCV
- PIL (Pillow)
- Google Generative AI (Gemini)
- Requests

