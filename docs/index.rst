.. mail_cleaner documentation master file, created by startproject.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mail-cleaner's documentation!
========================================

|build-status| |code-quality| |black| |coverage| |docs|

|python-versions| |django-versions| |pypi-version|

Handle and sanitize HTML & text emails

Features
========

* Sanitize untrusted links
* Best-effort plain-text message extraction from HTML e-mails

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |build-status| image:: https://github.com/maykinmedia/mail-cleaner/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/mail-cleaner/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/maykinmedia/mail-cleaner/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/mail-cleaner/actions?query=workflow%3A%22Code+quality+checks%22

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/maykinmedia/mail-cleaner/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/mail-cleaner
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/mail-cleaner/badge/?version=latest
    :target: https://mail-cleaner.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/mail-cleaner.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/mail-cleaner.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/mail-cleaner.svg
    :target: https://pypi.org/project/mail-cleaner/
