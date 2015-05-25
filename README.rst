Quick info
==========

Let say you need to use the HTTP load testing and benchmarking utility `siege`__ on a web page
and you also want to use the ``--internet`` option, to simulate at best the behavior of a web browser.

__ http://www.joedog.org/siege-home/

When a web browser load a page, it also load all the resources inside that page:

* Images
* JavaScript files
* CSS
* Media resources

So you need a list of all URLs taken from that page.

This utility (its name mean "**You Will Download**") will simply create this list for you.

You simply need to redirect the utility output to a file, then use also the siege ``--file`` option.

Usage
-----

::

    $ youlldownload http://host.com/section/page

Using with siege::

    $ youlldownload http://host.com/section/page > list.txt
    $ siege -i -f list.txt [other options]

Taken resouces
--------------

* from ``script`` tags we'll take the ``src`` URL
* from ``link`` tags with ``rel`` equals to ``stylesheet`` we'll take the ``href`` url
* from ``img`` tags we'll take the ``src`` URL
* from ``object`` tags we'll take the ``data`` URL
* from ``embed`` tags we'll take the ``src`` URL
* from ``style`` tags we'll take the URL inside if the tag is using an "*@import url*"
  directive
* from ``iframe`` tags we'll take the ``src`` URL
* from ``source`` tags inside ``video`` we'll take the ``src`` URL

Also: CSS sources are deeply analyzed for found additional resources inside them
(like background images, fonts, ...).

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
