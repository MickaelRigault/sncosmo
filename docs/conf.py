# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
#
# Astropy documentation build configuration file.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this file.
#
# All configuration values have a default. Some values are defined in
# the global Astropy configuration which is loaded here before anything else. 
# See astropy.sphinx.conf for which values are set there.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('..'))
# IMPORTANT: the above commented section was generated by sphinx-quickstart, but
# is *NOT* appropriate for astropy or Astropy affiliated packages. It is left
# commented out with this explanation to make it clear why this should not be
# done. If the sys.path entry above is added, when the astropy.sphinx.conf
# import occurs, it will import the *source* version of astropy instead of the
# version installed (if invoked as "make html" or directly with sphinx), or the
# version in the build directory (if "python setup.py build_sphinx" is used).
# Thus, any C-extensions that are needed to build the documentation will *not*
# be accessible, and the documentation will not build correctly.

# Load all of the global Astropy configuration
from astropy.sphinx.conf import *

# TODO: remove this once astropy#1841 is merged
intersphinx_mapping['astropy'] = ('http://docs.astropy.org/en/stable/', None)

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.1'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns.append('_templates')

# This is added to the end of RST files - a good place to put substitutions to
# be used globally.
rst_epilog += """
"""

# -- Project information ------------------------------------------------------

# This does not *have* to match the package name, but typically does
project = u'sncosmo'
author = u'Kyle Barbary and contributors'
copyright = u'2013, ' + author

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

import sncosmo
# The short X.Y version.
version = sncosmo.__version__.split('-', 1)[0]
# The full version, including alpha/beta/rc tags.
release = sncosmo.__version__

# -- Settings for extensions and extension options -----------------------------

# replace viewcode extension with patched version.
# This can be removed once the following issue is fixed in sphinx:
#
# https://bitbucket.org/birkenfeld/sphinx/issue/623/
# extension-viewcode-fails-with-function
#
# (See above comments for being careful with sys.path)
import sys
import os
sys.path.append(os.path.abspath('ext'))
extensions.remove('sphinx.ext.viewcode')
extensions.append('viewcode')

# -- Options for HTML output ---------------------------------------------------

# A NOTE ON HTML THEMES
# The global astropy configuration uses a custom theme, 'bootstrap-astropy',
# which is installed along with astropy. A different theme can be used or
# the options for this theme can be modified by overriding some of the
# variables set in the global configuration. The variables set in the
# global configuration are listed below, commented out.

html_theme_options = {
    'logotext1': 'sn',     # white,  semi-bold
    'logotext2': 'cosmo',  # orange, light
    'logotext3': ''        # white,  light
    }

# Add any paths that contain custom themes here, relative to this directory.
# To use a different custom theme, add the directory containing the theme.
#html_theme_path = []

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes. To override the custom theme, set this to the
# name of a builtin theme or the name of a custom theme in html_theme_path.
#html_theme = None

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}
html_sidebars = {
    '**': ['globaltoc.html'],
#    'search': [],
#    'genindex': [],
#    'py-modindex': [],
}

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'sncosmo_logo_32.ico'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = ''

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = '{0} v{1}'.format(project, release)

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'

# Add local templates path to modify autosummary templates
#templates_path = ['_templates']
if 'templates_path' not in locals():  # in case parent conf.py defines it
    templates_path = []
templates_path.append('_templates')

# Static files to copy after template files
html_static_path = ['_static']
html_style = 'sncosmo.css'

# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [('index', project + '.tex', project + u' Documentation',
                    author, 'manual')]


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [('index', project.lower(), project + u' Documentation',
              [author], 1)]
