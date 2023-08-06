from enum import Enum
from typing import Union

from PIL import Image

from img_ai_prep.center_detection import face_center
from img_ai_prep.crop import crop
from img_ai_prep.resize import resize


class CropMode(Enum):
    resize_center_crop = 0
    face_center_crop = 1
    entropy_resize_crop = 2
    noresize_center_crop = 3
    noresize_face_center = 4


def img_ai_prep(input_image: Image.Image,
                final_size: int,
                crop_mode: Union[CropMode, str] = CropMode.resize_center_crop,
                **kwargs) -> Image.Image:
    if isinstance(crop_mode, str):
        if crop_mode not in CropMode.__members__:
            raise ValueError("Invalid Crop mode")
        crop_mode = CropMode[crop_mode]

    if crop_mode == CropMode.resize_center_crop:
        return crop(resize(input_image, final_size), center=None,
                    crop_size=final_size)
    elif crop_mode == CropMode.noresize_center_crop:
        return crop(input_image, center=None, crop_size=final_size)
    elif crop_mode == CropMode.face_center_crop:
        resized_img = resize(input_image, final_size)
        center = list(face_center(resized_img, **kwargs))
        return crop(resized_img, center=center,
                    crop_size=final_size)
    elif crop_mode == CropMode.noresize_face_center:
        center = list(face_center(input_image, **kwargs))
        return crop(input_image, center=center,
                    crop_size=final_size)
    else:
        print("WARN: Unknown crop mode")
