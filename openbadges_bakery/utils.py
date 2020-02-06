

import re
from xml.dom.minidom import parseString

from . import png_bakery, svg_bakery


def check_image_type(image_file):
    if image_file.read(8) == b'\x89PNG\r\n\x1a\n':
        return 'PNG'
    image_file.seek(0)
    # TODO: Use xml library to more accurately detect SVG documents
    if re.search(b'<svg', image_file.read(256)):
        return 'SVG'

def unbake(image_file):
    """
    Return the openbadges content contained in a baked image.
    """
    image_type = check_image_type(image_file)
    image_file.seek(0)
    if image_type == 'PNG':
        return png_bakery.unbake(image_file)
    elif image_type == 'SVG':
        return svg_bakery.unbake(image_file)

def bake(image_file, assertion_json_string, output_file=None):
    """
    Embeds a serialized representation of a badge instance in an image file.
    """
    image_type = check_image_type(image_file)
    image_file.seek(0)
    if image_type == 'PNG':
        return png_bakery.bake(image_file, assertion_json_string, output_file)
    elif image_type == 'SVG':
        return svg_bakery.bake(image_file, assertion_json_string, output_file)
