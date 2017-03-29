import codecs
import hashlib
import json
from tempfile import NamedTemporaryFile
from xml.dom.minidom import parseString


def bake(imageFile, assertion_string, new_file=None):

    svg_doc = parseString(imageFile.read())
    imageFile.close()

    assertion_node = svg_doc.createElement('openbadges:assertion')
    assertion_node = _populate_assertion_node(assertion_node, assertion_string,
                                              svg_doc)

    svg_body = svg_doc.getElementsByTagName('svg')[0]
    svg_body.setAttribute('xmlns:openbadges', "http://openbadges.org")
    svg_body.insertBefore(assertion_node, svg_body.firstChild)

    if new_file is None:
        new_file = NamedTemporaryFile(suffix='.png')

    new_file.write(svg_doc.toxml('utf-8'))
    new_file.seek(0)
    return new_file


def _populate_assertion_node(assertion_node, assertion_string, svg_doc):
    try:
        assertion = json.loads(assertion_string)
    except ValueError:
        assertion = None

    if assertion:
        verify_url = assertion.get('verify', {}).get('url')
        if verify_url:
            assertion_node.setAttribute('verify', verify_url)
        else:
            # TODO: Support 0.5 badges
            pass
        character_data = svg_doc.createCDATASection(assertion_string)
        assertion_node.appendChild(character_data)

    else:
        assertion_node.setAttribute('verify', assertion_string)

    return assertion_node


def unbake(imageFile):
    svg_doc = parseString(imageFile.read())

    assertion_node = svg_doc.getElementsByTagName("openbadges:assertion")[0]
    character_data = None
    for node in assertion_node.childNodes:
        if node.nodeType == node.CDATA_SECTION_NODE:
            character_data = node.nodeValue
    url = assertion_node.attributes['verify'].nodeValue.encode('utf-8')
    return character_data or url
