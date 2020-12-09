

import json
import os
import os.path

from unittest import TestCase
from xml.dom.minidom import parseString

from . import png_bakery
from . import utils

png_assertion = {
    "uid": "123",
    "issuedOn": "2015-04-01",
    "badge": "http://example.org/badge1",
    "recipient": {
        "identity": "test@example.com",
        "hashed": False
    },
    "verify": {
        "type": "hosted",
        "url": "http://example.org/badgeinstance1"
    }
}

svg_assertion = {
    "uid": "abcdef12345",
    "identity": {
        "recipient": "sha256$cbb08ce07dd7345341b9358abb810d29eb790fed",
        "type": "email",
        "hashed": True
    },
    "verify": {
        "type": "hosted",
        "url": "https://example.org/assertion.json"
    },
    "issuedOn": "2013-11-05",
    "badge": "https://example.org/badge.json"
}


class TypeDetectionTests(TestCase):

    def test_detect_svg_type(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'testfiles', 'baked_example.svg'
                               )) as image:
            self.assertEqual(utils.check_image_type(image), 'SVG')

    def test_detect_png_type(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'testfiles', 'public_domain_heart.png'
                               )) as image:
            self.assertEqual(utils.check_image_type(image), 'PNG')


class PNGBakingTests(TestCase):
    def test_bake_png(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'testfiles', 'public_domain_heart.png'
                               )) as image:

            return_file = png_bakery.bake(image, json.dumps(png_assertion))
            self.assertEqual(utils.check_image_type(return_file), 'PNG')
            return_file.seek(0)
            self.assertEqual(png_bakery.unbake(return_file),
                             json.dumps(png_assertion))

    def test_unbake_png(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'testfiles', 'baked_heart.png'
                               )) as image:
            assertion = png_bakery.unbake(image)
            self.assertEqual(json.loads(assertion), png_assertion)


class SVGBakingTests(TestCase):
    def test_bake_svg(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'testfiles', 'unbaked_example.svg'
                               )) as image:

            return_file = utils.bake(image, json.dumps(svg_assertion))
            self.assertEqual(utils.check_image_type(return_file), 'SVG')
            return_file.seek(0)
            self.assertEqual(utils.unbake(return_file), svg_assertion['verify']['url'])

    def test_unbake_svg(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'testfiles', 'baked_example.svg'
                               )) as image:
            verify_url = utils.unbake(image)
            self.assertEqual(verify_url, svg_assertion['verify']['url'])

    def test_svg_roundtrip_hosted(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'testfiles', 'unbaked_example.svg'
                               )) as image:

            svg_string = json.dumps(svg_assertion)
            return_file = utils.bake(image, svg_string)
            self.assertEqual(utils.check_image_type(return_file), 'SVG')
            return_file.seek(0)
            self.assertEqual(utils.unbake(return_file), svg_assertion['verify']['url'])

        return_file.seek(0)
        baked_xml = parseString(return_file.read())
        assertion_node = baked_xml.getElementsByTagName("openbadges:assertion")[0]
        self.assertEqual(assertion_node.attributes['verify'].value, svg_assertion['verify']['url'])

    def test_svg_roundtrip_signed(self):
        signed_string = 'eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ.dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'

        with open(os.path.join(os.path.dirname(__file__),
                               'testfiles', 'unbaked_example.svg'
                               )) as image:

            return_file = utils.bake(image, signed_string)

        return_file.seek(0)
        self.assertEqual(utils.unbake(return_file), signed_string)
