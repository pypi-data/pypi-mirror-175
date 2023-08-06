"""
Code for resizing images intelligently with minimal fidelity loss.
The idea is to resize the _shortest_ side to the desired size, allowing
secondary cropping to preserve maximum quality.
"""

from typing import Tuple

from PIL import Image


def resize_math(im_size: Tuple[int, int],
                new_long_side: int) -> Tuple[int, int]:
    if im_size[1] > im_size[0]:
        # Resize
        resize_key = im_size[0]
        percent = float(new_long_side) / float(resize_key)
        if percent > 1:
            print("INFO: Resizing image to be larger, results may be blurry")
        hsize = int((float(im_size[1]) * percent))
        return new_long_side, hsize

    else:
        resize_key = im_size[1]
        percent = float(new_long_side) / float(resize_key)
        if percent > 1:
            print("INFO: Resizing image to be larger, results may be blurry")
        hsize = int((float(im_size[0]) * percent))
        return hsize, new_long_side


def resize(_im: Image.Image,
           new_long_side: int = 1024,
           resize_method: Image.Resampling = Image.Resampling.LANCZOS
           ) -> Image.Image:
    resize_tuple = resize_math(_im.size, new_long_side)
    _newim = _im.resize(resize_tuple, resize_method)
    return _newim
