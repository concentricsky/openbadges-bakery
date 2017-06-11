import json
import os
import os.path

from unittest import TestCase

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
            self.assertEqual(utils.unbake(return_file),
                             json.dumps(svg_assertion))


    def test_unbake_svg(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'testfiles', 'baked_example.svg'
                               )) as image:
            assertion = utils.unbake(image)
            self.assertEqual(json.loads(assertion), svg_assertion)
