# Screen Detection - An Analysis of Possible Approaches

## Abstract
In this document, I am exploring different pipelines and approaches that could be used for Emblem's screen detection system. Primarily, I am considering approaches that would be practical for real-time detection from a webcam feed on a device without specialized hardware (i.e., crazy GPUs).

## Detectron2
**Very accurate, but too slow**
Detectron2 is a modular and scalable library developed by Facebook AI for object detection, instance segmentation, and other vision tasks, built on PyTorch. Its strengths include state-of-the-art accuracy, support for a wide range of tasks, and flexibility for customization, making it a favorite for research and production. However, its weaknesses are relatively slower inference speeds compared to lightweight models like YOLO and a higher reliance on GPUs for efficient performance.

Quick experiments with Detectron2 reflected these tradeoffs. The [playground demo](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5#scrollTo=8IRGo8d0qkgR) detected and classified monitors in a test image [very well](detectron2-classified.png), but took ~4 seconds to run and ~12s to visualize in a Google Colab with GPU. 

Overall, while it works "out of the box," Detectron2 is too slow for a real-time use case.

## Yolo
YOLO (You Only Look Once) is a family of single-stage object detection models designed for real-time performance and efficiency, with YOLOv8 being its latest iteration. Its strengths lie in fast inference speeds, simplicity, and compatibility with resource-constrained devices, making it ideal for real-time applications. However, it sacrifices some accuracy and flexibility compared to heavier, two-stage frameworks like Detectron2.

It is definitely fast enough - [this tutorial](https://www.youtube.com/watch?v=QV85eYOb7gk) is a good demonstation of how easy it is to integrate with OpenCV, and how fast it can run with a webcam. The trouble then is, how accurately can it detect a screen?

Note: this is a segmentation problem. The model needs to detect a screen from an image feed, and then segment that screen for emblem identification.

## Hardware Approach: Depth and IR
An IR camera would be very efficient at detecting screens, given that they ![emit IR light](https://images.squarespace-cdn.com/content/v1/60fac36ba4a38031ecc66f54/8ce94027-6823-46bf-81fd-6e04259b8e1e/IMG_20220708_191639.jpg?format=1000w). 

Likewise, a depth camera could probably help with detection, although I do not think it would be as beneficial as an IR camera.