.. MODBUS documentation master file, created by
   sphinx-quickstart on Tue Jul  6 13:54:49 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Modbus  documentation!
================================================
All modbus supported device will be interfaced using this module . Device configuration will be read for a particular device ID if configuration is available or new configuration will need to created using device service. Device Configuration – This will be predefined text document with all required configuration for a particular type of device. Each physical device will have a unique ID which will be used as reference for all other module.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   rst/ModbusWrapper
   rst/ModbusConfigJsonDecoder
   rst/modbus_config
   rst/ModbusPolling
  

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
