from typing import List, Tuple

from PIL import Image


def crop_math(im_size: Tuple[int, int],
              center: List[int],
              crop_size: int) -> Tuple[int, int, int, int]:
    # Move center if needed to keep full size crop
    if center[0] < int(crop_size / 2):
        center[0] = int(crop_size / 2)
    elif center[0] > (im_size[0] - int(crop_size / 2)):
        center[0] = im_size[0] - int(crop_size / 2)
    if center[1] < int(crop_size / 2):
        center[1] = int(crop_size / 2)
    elif center[1] > (im_size[1] - int(crop_size / 2)):
        center[1] = im_size[1] - int(crop_size / 2)

    # Identify the crop box
    left = max(0, int(center[0] - (crop_size / 2)))
    upper = max(0, int(center[1] - (crop_size / 2)))
    right = min(im_size[0], int(center[0] + (crop_size / 2)))
    lower = min(im_size[1], int(center[1] + (crop_size / 2)))
    box = (left, upper, right, lower)
    if box[2] - box[0] < crop_size or box[3] - box[1] < crop_size:
        print("INFO: Output image size less than desired")
    return box


def crop(im: Image.Image,
         center: List[int] = None,
         crop_size: int = 1024):
    if center is None:
        center = (int(im.size[0]/2), int(im.size[1]/2))
    box = crop_math(im.size, center=center, crop_size=crop_size)
    im = im.crop(box)
    return im
