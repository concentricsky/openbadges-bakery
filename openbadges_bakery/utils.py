import re
from xml.dom.minidom import parseString

import png_bakery


def check_image_type(imageFile):
    if imageFile.read(8) == '\x89PNG\r\n\x1a\n':
        return 'PNG'
    imageFile.seek(0)
    # TODO: Use xml library to more accurately detect SVG documents
    if re.search('<svg', imageFile.read(256)):
        return 'SVG'

def unbake(imageFile):
    """
    Return the openbadges content contained in a baked image.
    """
    image_type = check_image_type(imageFile)
    imageFile.seek(0)
    if image_type == 'PNG':
        return png_bakery.unbake(imageFile)
    elif image_type == 'SVG':
        return svg_bakery.unbake(imageFile)

def bake(imageFile, assertion_json_string):
    """
    Embeds a serialized representation of a badge instance in an image file.
    """
    image_type = check_image_type(imageFile)
    imageFile.seek(0)
    if image_type == 'PNG':
        return png_bakery.bake(imageFile, assertion_json_string)
    elif image_type == 'SVG':
        return svg_bakery.bake(imageFile, assertion_json_string)
