# img_ai_prep
More intelligently crop photos for ingestion to ML models. 
Supports two major workflows that will be useful to produce higher quality images:

### resize_center_crop
1. Resize the image with the shortest side matching the desired end size
2. Crop only the longer side to achieve final square image, preserving maximum content towards the center

### face_center_crop
1. Resize the image with the shortest side matching the desired end size
2. Crop towards detected faces in the image, preserving maximum human content

In addition to these enhanced cropping modes, the code also supports cropping towards faces without resizing, 
center cropping without resizing, 
and exposes the underlying `crop` and `resize` functions for use in your own workflows.

There is also support for easily passing custom models for face detection, and passing custom parameters to the models. 
Passing the model by argument also improves performance if you are working in a loop, 
as it does not need to read the model from disk every time if passed by argument.

## Usage
| Original Image                                                                           | noresize_center_crop                                               | resize_center_crop                                                         | face_center_crop                                                                     | noresize_face_center                                                   |
|------------------------------------------------------------------------------------------|--------------------------------------------------------------------|----------------------------------------------------------------------------|--------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| ![ original](/examples/example_photos/original/hugo_leonardo_de_souza_lopez_pixabay.jpg) | ![ center crop](/examples/example_photos/processed/naive_crop.jpg) | ![ resize crop](/examples/example_photos/processed/resize_center_crop.jpg) | ![ resize face crop](/examples/example_photos/processed/resize_face_center_crop.jpg) | ![ face crop](/examples/example_photos/processed/face_center_crop.jpg) |

Simply install with pip and get to processing your images!
```bash
pip install img_ai_prep
```

```python
from PIL import Image

from img_ai_prep import img_ai_prep

im = Image.open("input.jpg")
newimg = img_ai_prep(im,
                     final_size=1024,
                     crop_mode="resize_center_crop")
print(newimg.size)
newimg.save("output.jpg")
```

Advanced example script passing a custom model and parameters:
```python
import cv2
from PIL import Image

from img_ai_prep import img_ai_prep

if __name__ == "__main__":
    im = Image.open("my_img.jpg")

    model = cv2.CascadeClassifier(cv2.data.haarcascades +
                                  "haarcascade_frontalface_alt.xml")
    newimg = img_ai_prep(im,
                         final_size=1024,
                         crop_mode="face_center_crop",
                         model=model,
                         min_neighbors=50,
                         min_size=(100,100))
    print(newimg.size)
    newimg.save("my_output.jpg")
```
