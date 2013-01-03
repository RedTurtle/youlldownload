# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys, os

setup(name='YoullDownload',
      # scripts=['src/youlldownload.py',],
      version="0.1",
      description="Grab from a remote site page all resources that a browser "
                  "will probably download visiting the page",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=["Development Status :: 4 - Beta",
                   "License :: OSI Approved :: GNU General Public License (GPL)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2.7",
                   "Topic :: Utilities",
                   "Topic :: Internet :: WWW/HTTP",
                   ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='crawler log web',
      author='RedTurtle Technology',
      author_email='info@redturtle.it',
      url='https://github.com/RedTurtle/YoullDownload',
      license='GPL',
      # packages=find_packages('src', exclude=['ez_setup',]),
      py_modules=['youlldownload',],
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pyquery',
      ],
      entry_points={'console_scripts': ['youlldownload = youlldownload:main', ]}
      )
