
Open Badges Bakery
==================

This package contains the utilities needed to "bake" Open Badges metadata into
PNG or SVG image files or extract ('unbake') metada from such images.

This Open Badges Bakery is produced by Concentric Sky. https://concentricsky.com

Installation
------------

pip:

.. code:: bash

    pip install openbadges_bakery

Command Line Interface
----------------------

There is a command line interface for baking and unbaking assertion data. 

To bake a badge, identify the existing BadgeClass image with the input_filename
and desired baked Assertion image filename to be created as well as the data to
be baked into the image.

.. code:: bash

    bakery bake [input_filename] [output_filename] --data='{"data": "data"}'

To extract Open Badges data from an image, use the ``unbake`` command.

.. code:: bash

    bakery unbake [input_filename]

Output_filename is optional if you want the baked data to be written to a file.

.. code:: bash

    bakery unbake [input_filename] [output_filename]

Python Interface
----------------
The bake and unbake functions are available when installed as a python module

To bake a badge, pass in an open file as ``input_file`` and the string of the 
badge data you wish to bake into the image. Result is an open TemporaryFile
that contains the data.

.. code:: python

    from openbadges_bakery import bake
    output_file = bake(input_file, assertion_json_string)

To unbake a badge, pass in an open file as ``input_file``:

.. code:: python

    from openbadges_bakery import unbake
    output_file = unbake(input_file)
