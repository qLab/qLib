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
- **Usability**: our tools try to avoid the "in-house" look-and-feel

qLib is **open source software** licensed under the [New BSD
license](https://github.com/qLab/qLib/blob/master/LICENCE). It's developed by
VFX professionals from several studios working on feature films, game
cinematics and commercials.

[qLib Summary / Highlights (facebook)](https://www.facebook.com/notes/qlib/qlib-summary-highlights/726676570699463)


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


### Quick Installation

- Download the latest version (see link above)
- Extract and move it into the Houdini preferences folder in your home folder
- Append provided houdini.env example file contents to your own houdini.env
  - Alternatively, use a package json file (see below)


### Installation

#### 1. Getting qLib

You can either grab a compressed archive file (as mentioned above), or
you can clone the official repository with **git**.
(The archive way is the easiest, but with git you can update faster,
revert to previous versions quick, etc.)


#### 2. Adding it to the Houdini environment

##### Houdini 17.5 or higher ("plugin" method)

- Create a folder called **packages** in your Houdini preferences folder (in your home dir)
- Copy the **qLib_linux.json** (or **qLib_windows.json**) file into the **packages** folder
- Edit the json file to point to the extracted qLib folder (edit the path in the "QLIB" line)

[To read more on configuration, see the documentation on Packages](https://www.sidefx.com/docs/houdini/ref/plugins.html)

(Please note that qLib requires 17.5.321 or higher for its package to work.)

##### Older Houdini versions

We provide example *houdini.env* files (windows and linux) which can be
*appended to your houdini.env file in your Houdini preferences folder*
(the HoudiniXX.X/ folder in your home directory).

[To read more on configuration, see the documentation on houdini.env](http://www.sidefx.com/docs/houdini/basics/config_env)


#### 2a. Important note for facilities

If you're installing at a large facility with a package management system,
*do not rely on houdini.env files* --
use your package manager to set up environment variables.


### Further readings and other places of interest

qLib comes with documentation. All assets have help cards (even with
example images and whatnot), providing all the related important details.

We appreciate bug reports, RFEs (Request For Enhancement), or feedback of
any kind.
[Our issue tracker is here](https://github.com/qLab/qLib/issues?state=open).

If you need help, have a question or just want to keep up with the news
regarding qLib, feel free to join us on our [Google
Groups](https://groups.google.com/forum/#!forum/qlib) page.

#### Thank you for your interest in qLib!
##### The qLib Team

