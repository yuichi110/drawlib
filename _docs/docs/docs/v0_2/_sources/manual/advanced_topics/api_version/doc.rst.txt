==================
Using Old APIs
==================

Software library has dillenma.
That is

- Improvement of library API is required
- But old user want to keep old APIs since their old code doesn't work with new API

drawlib has same problems too.

Matured library such as ``requests`` doesn't change their core API.
More new library will change their API sometimes.
On that time, they requests users to

- change user code
- use old version library

drawlib is not matured library now.
So we want to change API for future improvement.
But we don't want to let user use old library.
So, drawlib adopt API versioning inside the library.
It means drawlib new library holds not only new API, but also old API too.

In previous example, we imported library as ``from drawlib.advance import *``.
It will import latest API on the library.
If you use drawlib version 0.5, API version 0.5 are imported.

But you can import old library as ``from drawlib.<old_version>.advance import *``.
With specifying API version in package, you can use old API at new library.

For example, when you create your code with ``drawlib version 0.1``.
Few years later, you want to run your code at ``drawlib version 0.5``.
On this situation you can import like this.

.. code-block:: python

    from drawlib.v0_1.advance import *

Your code will run with ``API version 0.1`` on ``drawlib version 0.5`` which is almost same to ``drawlib version 0.1``.
If you like conservertive code, you should specify import version when you write your code.

You can do same for using ``drawlib`` command.

.. code-block:: bash

    python -m drawlib.v0_1 <args>

It will call API version 0.1 on drawlib version 0.5 too.

We will not touch old API code after new version release.
Only if critical bug fix is required, it can be modified without changing API.

However, when the API becomes too old for new Python or underlying library Matplotlib, we will depricate the API version.
On that situation, please get old drawlib library for run old code.

Drawlib's versioning is ``major.minor.patch``.
patch release doesn't have API change.
version ``0.1.1`` and ``0.1.5`` has same API.
So you can't specify patch version at import.