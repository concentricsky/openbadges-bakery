

import codecs
import hashlib
from io import BytesIO, StringIO
import itertools
import os.path
import png
import re
from tempfile import NamedTemporaryFile


def unbake(imageFile):
    """
    Return the openbadges content contained in a baked PNG file.
    If this doesn't work, return None.

    If there is both an iTXt and tEXt chunk with keyword openbadges,
    the iTXt chunk content will be returned.
    """

    reader = png.Reader(file=imageFile)
    for chunktype, content in reader.chunks():
        if chunktype == b'iTXt' and content.startswith(b'openbadges\x00'):
            return re.sub(b'openbadges[\x00]+', b'', content).decode('utf8')
        elif chunktype == b'tEXt' and content.startswith(b'openbadges\x00'):
            return content.split(b'\x00')[1].decode('utf8')


def bake(imageFile, assertion_string, newfile=None):
    """
    Embeds a serialized representation of a badge instance in a PNG image file.
    """
    encoded_assertion_string = codecs.getwriter('utf-8')(assertion_string)
    reader = png.Reader(file=imageFile)

    if newfile is None:
        newfile = NamedTemporaryFile(suffix='.png')

    chunkheader = b'openbadges\x00\x00\x00\x00\x00'
    chunk_content = chunkheader + encoded_assertion_string.stream.encode('utf-8')
    badge_chunk = (b'iTXt', chunk_content)
    png.write_chunks(newfile, baked_chunks(reader.chunks(), badge_chunk))

    newfile.seek(0)
    return newfile


def baked_chunks(original_chunks, badge_chunk):
    """
    Returns an iterable of chunks that places the Open Badges baked chunk
    and filters out any previous Open Badges chunk that may have existed.
    """
    def is_not_previous_assertion(chunk):
        if chunk[1].startswith(b'openbadges\x00'):
            return False
        return True

    first_slice = next(original_chunks)
    last_slice = list(filter(
        is_not_previous_assertion,
        original_chunks
    ))

    return itertools.chain([first_slice], [badge_chunk], last_slice)
