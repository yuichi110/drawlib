===============
Install
===============

You can install drawlib with the following command. If your system uses ``python3`` and ``pip3``, use them instead.

.. code-block:: none

   $ pip install drawlib

After installation, you can check whether Drawlib was installed successfully with these commands:

.. code-block:: none

   $ python -m drawlib --version
   software=0.1.24
   api=0.1.24

   $ drawlib --version 
   software=0.1.24
   api=0.1.24

The Drawlib package also installs the ``drawlib`` command, which is useful for building many images. 
This command calls the Drawlib libraries' script, equivalent to ``python -m drawlib``. 
For more details, refer to the relevant section in the foundation chapter.

In addition to the software (library) version, you can also see the API version. 
This is because Drawlib supports old APIs (previously released library APIs) in new versions for backward compatibility. 
You can specify the Drawlib API version like this:

.. code-block:: none

   $ python -m drawlib.v0_1 --version
   software=0.1.24
   api=0.1.24

Troubleshooting
-------------------

Drawlib depends on ``matplotlib``, which requires ``msvc-runtime`` on Windows. 
If it is not automatically installed, you may encounter the following error when you try to draw:

.. code-block:: none

   ImportError: DLL load failed while importing _cext: The specified module could not be found

In this situation, please manually install ``msvc-runtime``:

.. code-block:: none

   pip install msvc-runtime

If you encounter another error, please check if your Python environment is either too old or too new.

Versioning 
===========

Drawlib follows the versioning rule ``<major>.<minor>.<patch>``. 

- Major Version: Significant API change
- Minor Version: Minor API change
- Patch Version: Bug fixes, etc. No API change

If you intend to use drawlib with a long-term project, we recommend installing a specific version with ``requirements.txt``.

.. code-block:: none

   drawlib == 0.1.*
   sphinx == 7.2.*
   sphinx-rtd-theme == 2.0.*

You can install or update these packages with the following command:

.. code-block:: none

   $ pip install -U -r requirements.txt

As you can see, the patch version is not specified, allowing bug fixes to be updated without any API changes. 
We recommend specifying not only the version of Drawlib but also the versions of the documentation building tools (like Sphinx) to ensure compatibility and stability.

Release policy
=================

Drawlib's release process is as follows:

* 0.1.* : private alpha release
* 0.2.* : public beta release
* 0.n.* : public releases
* n.m.* : matured public releases

After the public release of 0.3, each version will have development releases, such as:

* 0.3.0.dev1
* 0.3.0.dev2
* 0.3.0.dev<n>

As you can see, the patch version is 0, followed by ``dev<n>``. 
These are under-development testing releases for library developers and power users. 
You can't install them via pip normally, but you can install them by specifying the exact version:

.. code-block:: none

   $ pip install drawlib == 0.3.0.dev1

After the under-development phase ends, an official version like "0.3.1" will be released.

Once Drawlib matures, we will move to version "1.0.*" and later. 
Here is a release plan image:

.. figure:: image1.png
    :width: 600
    :class: with-border
    :align: center

    image1.png

Unfortunately, we do not plan to publish new fixes for older versions. 
This means that after releasing version 0.n.0, we will not provide new patch releases for ``0.<n-1>.*``.

Virtual Environment
=====================

If you have multiple documentation projects on your machine, we recommend installing Drawlib in a Python virtual environment, such as ``venv`` or ``poetry``. 
We typically use ``venv`` for pure documentation projects and ``poetry`` for development projects that involve documentation.

Using virtual environments allows you to isolate Drawlib installations for different projects, which helps avoid conflicts with underlying library versions like matplotlib.