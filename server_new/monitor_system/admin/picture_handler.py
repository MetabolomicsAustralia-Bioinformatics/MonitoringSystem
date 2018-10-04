import os
from PIL import Image

from flask import current_app


def add_pic(pic_upload, o_name):
    filename = pic_upload.filename
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    storage_filename = str(o_name) + '.' + ext_type

    filepath = os.path.join(current_app.root_path, 'static\organisation_pics', storage_filename)


    # Open the picture and save it
    pic = Image.open(pic_upload)

    pic.save(filepath)

    return storage_filename
