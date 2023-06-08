from PIL import Image
import sys
import glob
from PIL import ImageOps

# Trim all png images with white background in a folder
# Usage "python PNGWhiteTrim.py ../someFolder"

for filePath in sys.argv[1:]:


    image=Image.open(filePath)
    image.load()
    imageSize = image.size

    # remove alpha channel
    invert_im = image.convert("RGB") 

    # invert image (so that white is 0)
    invert_im = ImageOps.invert(invert_im)
    imageBox = invert_im.getbbox()

    image=image.crop(imageBox)

    newData = []
    for item in image.getdata():
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    image.putdata(newData)
    
    # save new image
    image.save(filePath)

