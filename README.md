# python-pdf-with-signature
This is more of a note to self than a library of solutions

The below pdfjinja readme is taken from https://github.com/yoongkang/pdfjinja

pdfjinja
========

.. image:: https://img.shields.io/badge/License-MIT%20License-blue.svg
  :target: https://raw.githubusercontent.com/rammie/pdfjinja/master/LICENSE

.. image:: https://api.travis-ci.org/rammie/pdfjinja.png?branch=master
  :target: https://travis-ci.org/rammie/pdfjinja


Use jinja templates to fill and sign PDF forms.

You can use this library to fill out a PDF form using data from an external
source such as a database or an excel file. Use a PDF editing software to edit
the form and specifiy a jinja template in the tooltip property of the form
field.


Dependencies
------------

You'll need the pdftk library. If you want to paste images, you'll need whatever
dependencies are necessary for Pillow to load your preferred image format.
Most of the packages below are taken from the Pillow documentation. You don't
need all of them. In most cases, just pdftk will do.


Ubuntu::

    apt-get install python-dev python-pip libtiff5-dev libjpeg8-dev \
        zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev \
        tk8.6-dev python-tk pdftk libmagickwand-dev


OSX::

  * Install pdftk (https://www.pdflabs.com/tools/pdftk-server/).
  * Install dependencies for Pillow if you want to paste images.


Windows::

  * Install pdftk (https://www.pdflabs.com/tools/pdftk-server/).
  * Install dependencies for Pillow if you want to paste images.


Installation
------------

You can install pdfjinja with pip::

    $ pip install pdfjinja
    $ pdfjinja -h


Usage:
------

See examples/sample.pdf for an example of a pdf file with jinja templates.
The template strings are placed in the tooltip property for each form field
in the pdf.

See examples/output.pdf for the output. The data that the form is filled with
comes from examples/sample.json.


Basic::


    $ pdfjinja -j examples/simple.json examples/sample.pdf examples/output.pdf

Attachments::

    $ pdfjinja --font examples/open-sans/regular.ttf \
               --json examples/sample.json \
               examples/sample.pdf \
               examples/output.pdf


Python::

    from pdfjinja import PdfJinja

    pdfjinja = PdfJinja('form.pdf')
    pdfout = pdfjinja(dict(firstName='Faye', lastName='Valentine'))
    pdfout.write(open('filled.pdf', 'wb'))


If you are using this with Flask as a webserver::

    from flask import current_app
    from pdfjinja import PdfJinja
    pdf = PdfJinja('form.pdf', current_app.jinja_env)


See examples/example.py for a more detailed python example. It might also be
helpful to example the sample pdf template in examples/sample.pdf.


What they don't tell you
========================

In Adobe Acrobat when creating a fillable pdf, you need to have the fields tooltip with variable set inside curly brackets like {{Name}} otherwise the dict that you pass pdfout (above) won't render correctly. 

![image](https://github.com/emg36/python-pdf-with-signature/blob/master/Screen%20Shot%202019-02-21%20at%2012.10.04%20PM.png)

I have updated the pdfjinja file to not input any data into the fields that don't have a bracket surrounded tooltip. 
I have also updated pdfjinja file to use 'On' as the value for checkboxes because that's the default that Adobe uses, not the "Yes" value it did have. As I will be using other people to create the pdf fillable fields I want there job to be as easy as possible, hence using another library. Another caveat, the auto generated fields by Adobe contain some naming conventions that will break the pdf creation if missed e.g. having a period, slash or bracket in the variable {{some.variable}} {{some/variable}} or {{[some_variable]}} which are hard to miss when you are uploading so many. 


The Other PDF Library
=====================

[https://github.com/revolunet/pypdftk] is awesome. It uses the value of the pdf field "name" not the "tooltip" like the other library. It does not however provide an easy way to insert a signature. Apparently, it can using stamps but it was not obvious to me how to find the position on the pdf of the field to set the offset dynamically as needed for different pdf generation. It has reasonable docs about how to use it too.


Final Solution
==============

The setup
---------
Lets say I have a pdf file that has the fillable fields name, some_checkbox and Sig. The Adobe acrobat field properties will look like the following screenshot. "name" field has attributes (name = name and tooltip = name), "some_checkbox" field has the attributes (name = some_checkbox, tooltip = some_checkbox) and "Sig" field has the attributes (name = Sig, tooltip = {{Sig | paste}}).

![another_image](https://github.com/emg36/python-pdf-with-signature/blob/master/Screen%20Shot%202019-02-21%20at%2012.43.23%20PM.png)

The execution
-------------
Use pypdftk to fill in all fields bar the signature, don't flatten the file, and saves it somewhere. Pdfjinja picks up the file and adds a signature, it does flatten the file and saves it again.

```python
from pdfjinja import PdfJinja
import pypdftk
import os

test_data = {'name':'Elliot', 'some_checkbox':'On'}
generated_pdf = pypdftk.fill_form('pdfs/originals/test-pdf.pdf', test_data, flatten=False)
out_pdf = pypdftk.concat([generated_pdf], 'pdfs/complete/temp_file.pdf')

pdfjinja = PdfJinja('pdfs/complete/temp_file.pdf')
pdfout = pdfjinja(dict(Sig='the_path_to_signature.png'))
pdfout.write(open('pdfs/complete/final-result.pdf', 'wb'))

# then probably need to remove the temp_file
os.remove('pdfs/complete/temp_file.pdf')
```


Is it pretty or ideal?
======================

No. No it is not. But it does work. If you want to just use the pdfjinja library that's cool but I don't have control over the people setting up hundreds of fillable pdfs. Plus, I have already written a bunch of tests on upload that will work with pypdftk.


To do
=====

Test that I can install everything to pip in one go like pip install git+https://github.com/emg36/python-pdf-with-signature.git
