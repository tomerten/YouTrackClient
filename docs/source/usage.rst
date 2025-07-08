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

Examples
--------

The following example scripts are available in the ``examples/`` directory:

.. literalinclude:: ../../examples/create_issue.py
   :language: python
   :caption: create_issue.py - Create a new issue
   :linenos:

.. literalinclude:: ../../examples/add_comment.py
   :language: python
   :caption: add_comment.py - Add a comment to an issue
   :linenos:

.. literalinclude:: ../../examples/add_spent_time.py
   :language: python
   :caption: add_spent_time.py - Add spent time (work item) to an issue
   :linenos:

.. literalinclude:: ../../examples/list_issues.py
   :language: python
   :caption: list_issues.py - List all issues in a project
   :linenos:

.. literalinclude:: ../../examples/issues_resolved_between_dates.py
   :language: python
   :caption: issues_resolved_between_dates.py - List issues resolved between two dates
   :linenos:

.. literalinclude:: ../../examples/run_command.py
   :language: python
   :caption: run_command.py - Run a YouTrack command on an issue
   :linenos:

See the :doc:`api` for full API details and :doc:`cli` for CLI usage.
