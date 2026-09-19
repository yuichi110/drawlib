=================
CLI and Options
=================

drawlib Command
===================

Once drawlib is installed, you gain access to the ``drawlib`` command. 
This command is equivalent to invoking the drawlib module using ``python -m drawlib``.

You can develop your illustration code using either ``python <your_drawlib_code>`` or ``drawlib <your_drawlib_code_or_directory>``. 
If you are working with a single file that doesn't import any other files, there is minimal difference between using these commands.

However, significant differences arise when managing multiple illustration codes or referencing style code:

- The python command executes a single file.
- The ``drawlib`` command performs several tasks before executing your code:

  - It detects your package architecture and registers paths.
  - It executes all Python files found under the specified directory.
  - It can automatically apply ``clear()`` before executing each file.


For projects involving numerous illustrations, we strongly recommend using the ``drawlib`` command over ``python`` for its added convenience and automation features.


Sample
=========

We will cover how to build multiple illustrations in detail in the foundational chapter. 
Please refer to that section for comprehensive guidance. 
However, as demonstrated here, the ``drawlib`` command is capable of building multiple Python illustration codes after registering your package path.

.. code-block:: none

   $ drawlib docs/                
   Detect package root "/Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs".
      - Add parent directory of package root "/Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many" to Python Path.

   Execute python files
      - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/__init__.py
      - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/chap01/__init__.py
      - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/chap01/image1.py
      - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/chap01/image2.py
      - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/chap02/__init__.py
      - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/chap02/image1.py
      - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/commons/__init__.py
      - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/commons/style.py
      - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/commons/util.py


Command Options
==================

The ``drawlib`` command includes the ``-h`` and ``--help`` options, which display command help.

.. code-block:: none
    
    $ drawlib -h
    usage: drawlib [-h] [-v] [--purge_font_cache] [--disable_auto_clear] [--enable_auto_initialize] [--quiet] [--verbose] [--developer] ...

    Ilustration as code by python

    positional arguments:
    file_or_directory     Target python file or directory which contains python codes

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version         Show version.
    --purge_font_cache    Purge cached font files.
    --disable_auto_clear  Disable clearing canvas per executing drawing code files.
    --enable_auto_initialize
                            Enable initializing theme/canvas/image_cache per executing drawing code files.
    --quiet               Enable quiet logging. show only error messages
    --verbose             Enable verbose logging.
    --debug               Enable verbose logging. Equivalent to option "--verbose".
    --developer           Enable verbose logging. Disable error handling for library users.

Controlling Auto Clear and Initialize Feature
-----------------------------------------------

By default, auto ``clear()`` is enabled, meaning your previous drawing actions are erased before executing the next illustration code. 
This behavior is generally suitable for normal use cases.

However, if you intend to create a single illustration using multiple Python files, this auto clear feature may not be desirable. 
In such cases, you can disable it using ``--disable_auto_clear``.

The ``clear()`` function does not reset theme settings and image cache, as many users prefer to maintain consistent themes across multiple illustrations. 
If you need to completely initialize drawlib per illustration code execution, you can use ``--enable_auto_initialize``. 
This option ensures that drawlib calls ``dutil_canvas.initialize()`` every time your code files are executed.

Typically, you won't need to specify both options.


Purging Font Cache
--------------------

The ``--purge_font_cache`` option removes drawlib's cached font files from your local machine. 

Font files are downloaded and cached the first time you use a particular font, and this option deletes those cached files to reclaim disk space. 
The combined size of font files is usually under 100MB. 
Note that using Chinese or Japanese fonts may consume more space due to the large number of characters they include. 

Uninstalling drawlib also removes cached fonts, as drawlib stores font caches in its library directory.

Setting Log Level
--------------------

Options like ``--quiet``, ``--verbose``, ``--debug``, and ``--developer`` adjust the log level:

- ``--quiet``: Suppresses all output except errors.
- ``--verbose`` / ``--debug``: Provides verbose logging and includes stack traces for errors.
- ``--developer``: Provides verbose logging and offering detailed error dumps without error handling, suitable for advanced Python users troubleshooting issues.

Choose the appropriate log level based on your need for error visibility and troubleshooting depth.