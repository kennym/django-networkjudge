.. Competition Manager documentation master file, created by
   sphinx-quickstart on Sun Apr 17 22:23:52 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Network Judge Overview
======================

*Competition Manager* aims to be a tool for organizing short-span (1-5 hours) programming
competitions in a local network.

This means that participants are on-site and have a fixed time period (mostly 1-5
hours) and one computer to solve a number of problems.

Problems are solved by writing a program in one of the allowed languages, that
reads input according to the problem input specification and writes the
correct, corresponding output.

The judging is done by submitting the source code of the solution to the jury.
There the jury system compiles and runs the program and compares the program
output with the expected output.

This software can be used to handle the submission and judging during such
competitions.

It has web interfaces for the jury, the participants (their submissions and
clarification requests) and the public scoreboard.

--------
Features
--------

A global overview of the features that DOMjudge provides:
 * Automatic judging
 * Web interface for portability and simplicity
 * Detailed jury information (submissions, judgings) and options (rejudge, clarifications)
 * Powered by Open Source Software

------------
Requirements
------------

 * One machine to host the server
 * Compilers for the languages to support

---------
Table of contents
---------

.. toctree::
   :maxdepth: 2

   overview
   requirements
   technical_design
   features

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

