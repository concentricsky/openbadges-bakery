from xml.dom.minidom import parseString

from django.core.files.base import ContentFile


def bake(imageFile, assertion_json_string):
    svg_doc = parseString(imageFile.read())
    imageFile.close()

    assertion_node = svg_doc.createElement('openbadges:assertion')
    # TODO: Provide valid verify document
    assertion_node.setAttribute('verify', 'http://example.com/badge.json')
    character_data = svg_doc.createCDATASection(assertion_json_string)
    assertion_node.appendChild(character_data)

    svg_body = svg_doc.getElementsByTagName('svg')[0]
    svg_body.setAttribute('xmlns:openbadges', "http://openbadges.org")
    svg_body.insertBefore(assertion_node, svg_body.firstChild)

    new_file = ContentFile(svg_doc.toxml('utf-8'))
    new_file.close()
    return new_file


def unbake(imageFile):
    svg_doc = parseString(imageFile.read())

    assertion_node = svg_doc.getElementsByTagName("openbadges:assertion")[0]
    for node in assertion_node.childNodes:
        if node.nodeType == node.CDATA_SECTION_NODE:
            data = node.nodeValue
    url = assertion_node.attributes['verify'].nodeValue.encode('utf-8')
    return data
