"""
Module for storing util functions
"""
import os
import errno
import uuid
from flask import current_app


def silentremove(path):
    """
    silently removes a file
    """
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def save_image(args):
    """
    save_image. saves image uploads and returns the path
    """
    if args['image_file']:
        mime_type = args['image_file'].mimetype
        if mime_type == 'image/png' or mime_type == 'image/jpeg':
            if 'png' in mime_type:
                file_type = 'png'
            elif 'jpeg' in mime_type:
                file_type = 'jpeg'
            destination = os.path.join(
                current_app.config.get('DATA_FOLDER'), 'medias/')
            if not os.path.exists(destination):
                os.makedirs(destination)

            image_file = '%s%s' % (
                destination, '{0}.{1}'.format(uuid.uuid4(), file_type))
            args['image_file'].save(image_file)
            return image_file.replace('app', '')
    return None
