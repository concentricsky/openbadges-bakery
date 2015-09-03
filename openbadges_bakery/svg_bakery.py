import json

from xml.dom.minidom import parseString

from django.core.files.base import ContentFile


def bake(imageFile, assertion_string):
    svg_doc = parseString(imageFile.read())
    imageFile.close()

    assertion_node = svg_doc.createElement('openbadges:assertion')
    assertion_node.setAttribute('verify', _get_verify_string(assertion_string))

    character_data = svg_doc.createCDATASection(assertion_string)
    assertion_node.appendChild(character_data)

    svg_body = svg_doc.getElementsByTagName('svg')[0]
    svg_body.setAttribute('xmlns:openbadges', "http://openbadges.org")
    svg_body.insertBefore(assertion_node, svg_body.firstChild)

    new_file = ContentFile(svg_doc.toxml('utf-8'))
    new_file.close()
    return new_file


def _get_verify_string(assertion_string):
    try:
        assertion = json.loads(assertion_string)
    except ValueError:
        assertion = None

    if assertion:
        verify_url = assertion.get('verify', {}).get('url')
        if verify_url:
            return verify_url
        else:
            # TODO: Support 0.5 badges
            pass

    return assertion_string


def unbake(imageFile):
    svg_doc = parseString(imageFile.read())

    assertion_node = svg_doc.getElementsByTagName("openbadges:assertion")[0]
    for node in assertion_node.childNodes:
        if node.nodeType == node.CDATA_SECTION_NODE:
            data = node.nodeValue
    url = assertion_node.attributes['verify'].nodeValue.encode('utf-8')
    return data
