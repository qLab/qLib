qLib
====

A procedural asset library for SideFX Houdini.

- http://qlab.github.io/qLib/
- https://github.com/qLab/qLib
- https://www.facebook.com/qLibHoudini

Download the **latest version** here:
https://github.com/qLab/qLib/archive/master.zip


### About

qLib is a digital asset library for SideFX's Houdini.
It is a collection of tools designed to work flawlessly with each other
and Houdini's native toolset.
It is driven by (and used in) *real production environments*,
but at the same time it fully respects and conforms to all the important
Houdini concepts.

Strong emphasis on the following things:
- **Backwards-compatibility**: old scenes will _not_ break over time
- **Performance**: we press for VEX/multithreading as much as possible
- **Usability**: our tools avoid the "in-house" look-and-feel

qLib is **open source software** licensed under the [New BSD
license](https://github.com/qLab/qLib/blob/master/LICENCE). It's developed by
VFX professionals from several studios working on feature films, game
cinematics and commercials.


### Tools

- Generation, manipulation and visualization of geometry attributes and groups
- Boundary geometry generation and manipulation
- A complete deformer suite, implemented through a common deformer framework
- Reimplemented high-performance versions of certain original Houdini OPs
- Workflow-related tools
- A large collection of gallery items (node and subnet presets)
- Shelf tools
- Colour scemes, extra menu items
- Experimental extras

More details here:
https://www.facebook.com/notes/qlib/qlib-summary-highlights/726676570699463


### Quick Installation

- Download the latest dev-branch (see link above)
- Extract and move it into your Houdini config directory
- Append the provided houdini.env example file to your own houdini.env

(Note that the provided env file example is for linux.)


### Installation

The installation process involves two steps: **getting the contents** and
**setting up the environment** for Houdini.

#### 1. Getting the contents

You can either grab a compressed archive file (as mentioned above), or
you can clone the official repository with **git**.

The archive way is the easiest, but using git has additional benefits,
such as instant updates, easy access to older versions, other development
branches, etc.

#### 2. Adding it to the Houdini environment

For Houdini to access qLib components, the following environment variables
are to be set up:

- `HOUDINI_OTLSCAN_PATH`: the assets themselves
- `HOUDINI_GALLERY_PATH`: gallery items
- `HOUDINI_TOOLBAR_PATH`: shelf tools
- `HOUDINI_SCRIPT_PATH`: support scripts (optional)

(This is entirely optional, as by design there's almost zero dependency
between qLib assets. You can experiment with assets by loading them manually,
without setting up anything.)

The easiest way to do this is to put the following lines into your
<a href="http://www.sidefx.com/docs/current/basics/config_env">houdini.env</a>
file (linux):

```
QLIB=<<path to qLib install>>
QOTL=$QLIB/otls

# (linux)
HOUDINI_OTLSCAN_PATH = $QOTL/base:$QOTL/future:$QOTL/experimental:@/otls
HOUDINI_GALLERY_PATH = $QLIB/gallery:@/gallery
HOUDINI_TOOLBAR_PATH = $QLIB/toolbar:@/toolbar
HOUDINI_SCRIPT_PATH = $QLIB/scripts:@/scripts
```

Note that on Windows you should use semicolons instead of colons:

```
QLIB=<<path to qLib install>>
QOTL=$QLIB/otls

# (windows)
HOUDINI_OTLSCAN_PATH = $QOTL/base;$QOTL/future;$QOTL/experimental;@/otls
HOUDINI_GALLERY_PATH = $QLIB/gallery;@/gallery
HOUDINI_TOOLBAR_PATH = $QLIB/toolbar;@/toolbar
HOUDINI_SCRIPT_PATH = $QLIB/scripts;@/scripts
```
Set environment variables on osx depending on the shell you are using. For bash/ksh use:	export variable=value:

```
# (osx bash/ksh)
QLIB=<<path to qLib install>>
QOTL=$QLIB/otls

HOUDINI_OTLSCAN_PATH=$QOTL/base:$QOTL/future:$QOTL/experimental:@/otls
HOUDINI_GALLERY_PATH=$QLIB/gallery:@/gallery
HOUDINI_TOOLBAR_PATH=$QLIB/toolbar:@/toolbar
HOUDINI_SCRIPT_PATH=$QLIB/scripts:@/scripts
```
For csh/tcsh use: setenv variable value"

```
# (osx csh/tcsh)
QLIB <<path to qLib install>>
QOTL $QLIB/otls

setenv HOUDINI_OTLSCAN_PATH $QOTL/base:$QOTL/future:$QOTL/experimental:@/otls
setenv HOUDINI_GALLERY_PATH $QLIB/gallery:@/gallery
setenv HOUDINI_TOOLBAR_PATH $QLIB/toolbar:@/toolbar
setenv HOUDINI_SCRIPT_PATH $QLIB/scripts:@/scripts
```

#### 3. Extras

Extra menu items and color scemes can be found in the `menu/` and `config/` folders.
These can be copied or linked into the appropriate folders within the user's
houdiniXX.X/ preferences folder (e.g. $HOME/houdini15.0/config)


### Further readings and other places of interest

qLib comes with documentation. All assets have help cards (even with
example images and whatnot), providing all the related important details.

Other aspects of the library are covered in the
[Wiki](https://github.com/qLab/qLib/wiki).

We appreciate bug reports, RFEs (Request For Enhancement), or feedback of
any kind.
[Our issue tracker is here](https://github.com/qLab/qLib/issues?state=open).

If you need help, have a question or just want to keep up with the news
regarding qLib, feel free to join us on our [Google
Groups](https://groups.google.com/forum/#!forum/qlib) page.

#### Thank you for your interest in qLib!
##### The qLib Team

