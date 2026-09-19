===============
Drawing Text
===============

Drawing text requires understanding the following concepts:

* text(): Function for drawing text
* TextStyle: Style class for text
* font: How to specify fonts
* Theme's pre-defined styles

We will explain each of these concepts in this section.

text()
=========

Drawlib uses the ``text()`` function for drawing text. 
It takes the following arguments:

* xy: coordinate of drawing point
* text: text value
* size(optional): size of text font
* angle(optional): angle of text
* style(optional): text style

Font size can be changed with ``size``, but it can also be changed by the ``style`` attribute. 
We recommend using the style attribute rather than size.
Similar to how you shouldn't configure text size in HTML but should do it in CSS, it's best to handle text styling via the style attribute for better consistency and flexibility.

We will explain style later, so for now, we will focus on the other arguments. 
Here are three examples:

.. literalinclude:: image1.py
   :language: python
   :linenos:
   :caption: image1.py

Below is a figure illustrating these examples:

.. figure:: image1.png
   :width: 600
   :class: with-border
   :align: center

   text()

Drawlib's default theme uses the multilingual font "Noto Sans CJK Japanese". 
This is a popular sans-serif font that supports CJK (Chinese, Japanese, Korean) in addition to the alphabet. 
As the font name suggests, it prioritizes Japanese but typically does not conflict with Chinese and Korean.

Fonts that prioritize Chinese and Korean are also provided. 
Additionally, other local language fonts are available for languages not supported by the default font.

text_vertical()
==================

While it is not common in alphabetic languages, vertically aligned text is popular in a few languages, such as Japanese. 
We provide the ``text_vertical()`` function to achieve this. 
The arguments are exactly the same as those for ``text()``.

* xy: coordinate of drawing point
* text: text value
* size(optional): size of text font
* angle(optional): angle of text
* style(optional): text style

Here are three examples:

.. literalinclude:: image_vertical1.py
   :language: python
   :linenos:
   :caption: image_vertical1.py

Below is a figure illustrating these examples:

.. figure:: image_vertical1.png
   :width: 600
   :class: with-border
   :align: center

   text_vertical()

Please use ``halign="center"`` in TextStyle. 
It is the default value. 
Horizontal align left/right will work, but it does not look nice except with monospaced fonts.

TextStyle
===========

``TextStyle`` is style class for ``text()`` and ``text_vertical()``.
It encompasses many attributes, categorized into "alignment", "text style", and "text background style".

``TextStyle`` has these attributes.

* halign: Horizontal alignment of text. Options are "left", "center", "right".
* valign: Vertical alignment of text. Options are "bottom", "center", "top".
* color: Text color.
* size: Text size.
* font: Text font.
* bgalpha: Background alpha.
* bglwidth: Background line width.
* bglcolor: Background line color.
* bglstyle: Background line style. Options are "solid", "dashed", "dotted", "dashdot".
* bgfcolor: Background fill color.

The default alignment is "center" horizontally and "center" vertically. 
By default, no background is drawn.

Here are 2 examples.

.. literalinclude:: image_style1.py
   :language: python
   :linenos:
   :caption: image_style1.py

The left-side example configures alignment and text style, while the right-side example configures text background style.
Below is a figure illustrating these examples:

.. figure:: image_style1.png
   :width: 600
   :class: with-border
   :align: center

   TextStyle

In our opinion, there are few chances to use text background. 
Setting a white (or another canvas background color) background without a border can be useful for drawing text over shapes and lines in some situations.

Font
======

Drawlib specifies fonts from Drawlib's font library or from your own font files. 
Drawlib does not use system fonts installed on your PC because using system fonts may result in inconsistent rendering across different environments.

Basic Font Classes
--------------------

Drawlib includes these basic Font classes:

* Font
* FontSanSerif
* FontSerif
* FontMonoSpace
* FontSourceCode
* FontRoboto

These classes contain popular fonts or fonts preferred by the Drawlib team.

Local Language Fonts
----------------------

Additionally, Drawlib supports local language fonts:

* FontArabic
* FontBrahmic
* FontChinese
* FontJapanese
* FontKorean
* FontThai

If your preferred language is not supported, please let us know. 
However, we can only support open-source free fonts at the moment.
And currently, we use Google fonts.

Here are font examples.

.. literalinclude:: image_font1.py
   :language: python
   :linenos:
   :caption: image_font1.py

Below is a figure illustrating these examples:

.. figure:: image_font1.png
   :width: 600
   :class: with-border
   :align: center

   Fonts

To change the default font, refer to the theme documentation. 
The ``dtheme.allstyles.merge()`` function allows you to partially override pre-defined styles. 
If you provide a TextStyle with fonts, the pre-defined fonts will be overridden with your specified font.

Custom Font
-------------

Drawlib offers a wide range of fonts. 
However, if you want to use fonts that are not supported, use the ``FontFile`` class. 
This class can be used in place of the basic font classes and accepts a font file as an argument.

Here is an examples which uses font avenger.

.. literalinclude:: image_file1.py
   :language: python
   :linenos:
   :caption: image_file1.py

Below is a figure illustrating these examples:

.. figure:: image_file1.png
   :width: 600
   :class: with-border
   :align: center

   FontFile

You can check the list of fonts supported by Drawlib in the Font documentation.

Theme's pre-defined styles
==============================

Text in Drawlib can utilize pre-defined styles from the theme you select.

The style syntax is: ``<color>_<type>_<weight>``.
If the color and weight are default, they are not explicitly shown in the style name.
However, text styles do not use the type variations that are used for lines and shapes.

Each weight type variation includes different font weights:

- ``light``: Font weight light
- default: Font weight regular
- ``bold``: Font weight bold

Here is an example script that demonstrates the use of theme-defined text styles:

.. literalinclude:: image_theme1.py
   :language: python
   :linenos:
   :caption: image_theme1.py

Below is a figure illustrating these examples:

.. figure:: image_theme1.png
   :width: 600
   :class: with-border
   :align: center

   Theme's pre-defined styles