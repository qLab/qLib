qLib
====

A general-purpose Digital Asset library for Houdini.

Get social, 'like' it and whatnot:
- facebook: http://www.facebook.com/pages/qLib/145692112131248
- twitter:  http://twitter.com/#!/qLib_houdini


Installation instructions
=========================

Download and unpack the distribution tarball from:

http://qlab.github.com/qLib/

    NOTE: Do NOT USE THE "Download as .zip" button on github.com. Use the
    above link if you need the ready-to-use .otl files or use 'git clone'
    if you want to tinker with the sources.

    The repository stores the assets in a textual form, which can't be used in
    Houdini directly. See README.developer or the Wiki for instructions on
    building the actual OTL files from source.

Place the unpacked folder to a convenient location -- probably somewhere where
others can access it as well -- and add the qLib/otls/<section_name> (see below)
folder to the HOUDINI_OTLSCAN_PATH environment variable. Creating a variable
called QLIB can make adding the various sections a bit easier. For example the
next two lines adds all sections to the path:

    QLIB = /Users/mate/qLab/qLib/otls
    HOUDINI_OTLSCAN_PATH = @/otls:$QLIB/base:$QLIB/spec:$QLIB/future

On Windows you should use semicolon instead of colon for path separator:

    QLIB = /Users/mate/qLab/qLib/otls
    HOUDINI_OTLSCAN_PATH = @/otls;$QLIB/base;$QLIB/spec;$QLIB/future

(Dumping the OTL files into a folder which contains other OTLs is not a recommended
practice: it'll needlessly make maintenance of your assets more difficult.)


Sections
========

The asset library contains the following sections: base, spec, future, and
graveyard. The assets belonging the different sections are stored in
directories with the same name.

The 'base' assets are intended to be used as building blocks of more
complex networks.

The 'spec' assets are useful in specific situations and are probably less
useful as generic tools. You may decide if you want to add the 'spec' section
to your path or not. No assets in other sections should ever depend on assets
in this section.

The 'future' assets are still evolving and not yet integrated into the main
distribution. They may lack documentation or other requirements (that we agree
to be mandatory for an asset to be complete). We still release them so they
can be used (therefore more extensively tested).

In other words, 'future' is the alpha testing ground in the "release early,
release often" spirit.

The 'graveyard' section is the resting place for obsolete assets. We keep them
for compatibility reasons for a while. After that they get removed from
the distribution.



A note on interdependencies
===========================

Although we like to avoid any interdependencies of assets (except depending on
'base' assets), but it's not a rule set in stone. In a few cases
an asset might depend on another. This is always mentioned on the dependent
asset's help page. (But if you have the complete library installed -- which is
the reasonable thing to do --, you won't have any problems).

'Spec' assets are the exception: no other asset should depend on them.
