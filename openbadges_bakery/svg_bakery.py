

import json
import re
import rfc3986
import six
from tempfile import NamedTemporaryFile
from defusedxml.minidom import parseString


def _is_jws(value):
    jws_regex = re.compile(r'^[A-z0-9\-=]+.[A-z0-9\-=]+.[A-z0-9\-_=]+$')
    test_value = value
    if isinstance(value, bytes):
        test_value = value.decode()
    return bool(jws_regex.match(test_value))


def _is_url(value):
    ret = False
    try:
        if (
            (value and isinstance(value, six.string_types))
            and rfc3986.is_valid_uri(value, require_scheme=True)
            and rfc3986.uri_reference(value).scheme.lower() in ['http', 'https']
        ):
            ret = True
    except ValueError:
        pass
    return ret


def bake(image_file, assertion_string, new_file=None):

    svg_doc = parseString(image_file.read())
    image_file.close()

    assertion_node = svg_doc.createElement('openbadges:assertion')
    assertion_node = _populate_assertion_node(assertion_node, assertion_string,
                                              svg_doc)

    svg_body = svg_doc.getElementsByTagName('svg')[0]
    svg_body.setAttribute('xmlns:openbadges', "http://openbadges.org")
    svg_body.insertBefore(assertion_node, svg_body.firstChild)

    if new_file is None:
        new_file = NamedTemporaryFile(suffix='.svg')

    new_file.write(svg_doc.toxml('utf-8'))
    new_file.seek(0)
    return new_file


def _populate_assertion_node(assertion_node, assertion_string, svg_doc):
    assertion = None
    verify_attr = None

    try:
        assertion = json.loads(assertion_string)
    except ValueError:
        pass

    if assertion:
        verify_attr = assertion.get('id')
        if verify_attr is None or not _is_url(verify_attr):  # For hosted badges, use verification URL
            verify_attr = assertion.get('verify', {}).get('url')

    elif _is_jws(assertion_string):  # For signed badges, embed JWS as verify attribute
        verify_attr = assertion_string

    elif _is_url(assertion_string):  # For 0.5 badges, the baking input is the url itself
        verify_attr = assertion_string

    if verify_attr:
        assertion_node.setAttribute('verify', verify_attr)

    character_data = svg_doc.createCDATASection(assertion_string)
    assertion_node.appendChild(character_data)

    return assertion_node


def unbake(image_file):
    svg_doc = parseString(image_file.read())

    assertion_node = svg_doc.getElementsByTagName("openbadges:assertion")[0]
    character_data = None
    verification_data = None
    for node in assertion_node.childNodes:
        if node.nodeType == node.CDATA_SECTION_NODE:
            character_data = node.nodeValue
    try:
        verification_data = assertion_node.attributes['verify'].nodeValue.encode('utf-8')
    except KeyError:
        pass
    return verification_data or character_data
