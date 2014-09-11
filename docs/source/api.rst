.. _api:

Developer Interface
===================

.. module:: bitstamp

Bitstamp
--------

.. autoclass:: bitstamp.Bitstamp
   :inherited-members:


Resources
---------

All resources have same attributs that Bitstamp API return.
Timestamp attributs have equivalent :code:`<attribut_name>_as_datetime` methods.

Exceptions
----------

.. autoexception:: bitstamp.exceptions.ParametersError
.. autoexception:: bitstamp.exceptions.MissingCredentials
