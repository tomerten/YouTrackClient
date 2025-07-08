Usage Guide
===========

Installation
------------

.. code-block:: bash

   poetry add youtrack-client

Quickstart
----------

.. code-block:: python

   from youtrack.client import YouTrackClient
   client = YouTrackClient(base_url='https://your-youtrack-instance', token='perm:XXXX')
   issues = client.get_issues(project_id='PROJECT')
   print(issues)

See the :doc:`api` for full API details and :doc:`cli` for CLI usage.
