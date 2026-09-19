===================
Debugging errors
===================

Drawlib hides detailed errors when user code encounters issues. 
At such times, Drawlib only displays:

- The file and line where the problem occurred
- The type of error that happened

This means Drawlib does not show the stack trace or where the library code encountered an error due to user input. 
We believe that showing detailed errors and the internal workings of Drawlib is not beneficial for ordinary users.

However, sometimes you may want to check the details. In such situations, you need to enable debug mode.

How to Enable Debug Mode
============================

Drawlib controls which output is shown on the console via logging levels. 
Detailed error logs are shown only at the debug logging level.

To set the logging level to debug, you have two options:

- Set the logging level by calling a function: ``dutil_settings.set_logging_mode("debug")``
- Set the logging level via CLI options: ``drawlib --verbose`` or ``drawlib --debug``

Please check the settings documentation and CLI options documentation for more details.
