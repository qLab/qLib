qLib
====

A procedural asset library for SideFX Houdini

### About

qLib is a **procedural** digital asset library for SideFX's Houdini. In the
right hands it can **speed up** the production process dramatically by letting
the **artist** spend more time on **what** she wants to achieve instead of
**how** she wants to achieve it. We call it procedural because it is a
collection of simple tools designed to work flawlessly with each other and
Houdini's native toolset. 

qLib is **open source software** licensed under the [New BSD
license](https://github.com/qLab/qLib/blob/master/LICENCE). It's developed by
VFX professionals from several studios working on feature films, game
cinematics and commercials.

### Installation

The installation process involves two steps: **getting the contents** and
**setting up the environment** for Houdini.

There are two ways to get the contents of the library. You can download a
compressed **archive file** or you can clone the official repository with
**Git**. While installing from an archive may be a bit simpler, we highly
recommend you to use **Git** since it gives you the additional benefits of
**instant updates** and easy access to **older versions** and **development
branches**.

### From Archive File

Simply **download**  the current version by pressing one of the download
buttons and **unpack** it to the place where you want to install qLib.

### Cloning the repository with Git

In order to use Git, you first have to **install** it.  Every modern **Linux**
distribution has a Git package.  Use your choice of package manager to install
it. On **Windows** download and install [Git on Windows](http://msysgit.github.com/),
on **OS X** do the same with
[git-osx-installer](http://code.google.com/p/git-osx-installer/).

After installing Git, open a terminal and **clone** the repository.  On
**Windows** use **git bash** which is a pretty decent shell included in **Git
on Windows**. Go to the directory where you want to install qLib and run **git
clone** with the url of the repository.

```
$ cd **PLACE/TO/INSTALL**
$ git clone https://github.com/qLab/qLib.git
```

Later if you want to update the library just go into your cloned repository and
run **git pull**.

```
$ cd qLib $ git pull
```

### Setting up the environment

To finish the installation you must tell Houdini to load the assets by setting
the **HOUDINI_OTLSCAN_PATH** environment variable. You can **skip** or
**postpone** this step if you want to try out individual assets by loading them
manually.

The easiest way to do this is to put the following lines into your <a
href="http://www.sidefx.com/docs/current/basics/config_env">
**houdini.env**</a> file:

```
QLIB=**PLACE/TO/INSTALL** QL_OTLS=$QLIB/otls
HOUDINI_OTLSCAN_PATH=@/otls:$QL_OTLS/base:$QL_OTLS/spec:$QL_OTLS/future
```

Note that on Windows you should use semicolons instead of colons as path
separator, so the **last line** on Windows should look like this:

```
HOUDINI_OTLSCAN_PATH=@/otls;$QL_OTLS/base;$QL_OTLS/spec;$QL_OTLS/future
```

### Further readings and other places of interest

qLib comes with fairly extensive **documentation**.  First and foremost every
asset should have a **help card** describing the asset's functionality and
behavior.

Other aspects of the library are covered in the
[Wiki](https://github.com/qLab/qLib/wiki).

If you think you ran into a **bug**, please report it on the project's [issue
tracker](https://github.com/qLab/qLib/issues?state=open).  **RFE**s are also
welcome there!

If you need help, have a question or just want to keep up with the news
regarding qLib, feel free to join us on our [Google
Groups](https://groups.google.com/forum/#!forum/qlib) page.

#### Thank you for your interest in qLib!
##### The qLib Team
