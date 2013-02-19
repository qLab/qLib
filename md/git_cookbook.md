Git and Github cookbook
=======================

### Introduction

This is a fast and dirty cookbook for qLib developers. Your username will be
**'Harry'** in this guide. Change it to your own when you execute the examples here.

### Create an account on Github

In order to use Github you have to make an account.

### Install Git


#### Ubuntu

```
$ sodo apt-get install git
```

On older Ubuntu versions:

```
$ sudo apt-get install git-core
```

#### Windows

Download and install [Git on Windows](http://msysgit.github.com/)

#### OS X

Download and install [git-osx-installer](http://code.google.com/p/git-osx-installer/)

### **Fork** the *qLab repository*

1. Search on Github for **qLab/qLib**.
2. Go to the page and press the **Fork button** near to the upper right.
3. Select your username as the destination.

Now you have your personal copy of the repository. You can not modify it
directly on Github, but you **can push** into it from a local clone on your
computer.  

You **can't** push into qLab's version of the repository.

### **Clone** *your* repository

```
$ git clone https://github.com/harry/qLib.git
```

This will create a directory in your current directory named 'qLib'. That
directory is your local copy of the repository.

Renaming or moving this directory won't affect it's inner workings.

```
mv qLib qLib-harry
```

You can also give a different name to it during cloning.

```
$ git clone https://github.com/harry/qLib.git qLib-harry
```


### **Peeking** around in your repository

Getting the current **status** of your **working directory** and **stage**:

```
$ git status
```

To read the **commit log**:

```
$ git log
```

To read about the last commit:

```
$ git log -1
```


### Setting up **remotes**

You can see **all** your defined remotes:

```
$ git remote show
```

The **clone** command automatically created a remote called *origin* that
points to the repository from where you cloned your local one.

To get **detailed information** about a remote

```
$ git remote show origin
```

If you want to pull changes from other remotes you have to **add** them. For
example if you want to track the development in the original qLib repository
you have to add it as a remote.

```
$ git remote add qLib-qLab https://github.com/qLab/qLib.git
```

Now you can pull the changes from there. If this is not the default remote for
the branch, you will have to tell Git which one you mean (master).

```
$ git pull qLab master
```


### Setting up **branches**

To list your **local branches**:

```
$ git branch
```

To list all branches, local and remote ones:

```
$ git branch -a
```

The **clone** command will only set up the default branch which is usually
called *master*. The *master* branch is usually the released version of the
content while development happens in other branches.

This is exactly the case with qLib too. Main development happens inside the
branch named `dev-MAJOR.MINOR.MAINTENANCE`, where MAJOR, MINOR and MAINTENANCE
are placeholders for actual version numbers.

The easiest way to set up a **tracking branch** is to use the *checkout* command
with the *-b* flag.

```
$ git checkout -b dev-0.2 origin/dev-0.2
```

The command above will create a **local branch** that pulls and pushes from and
to your repository on Github.

The difference between **local** and **remote** branches is that you can modify
a local branch directly while a remote branch is a read-only version of the
branch that is identical to the one on the remote at the moment of clone or
**fetch** operation.

The difference between a **tracking** and an ordinary branch is that the
tracking branch 'knows' from where to pull or where to push. You can pull and
push from an ordinary branch too, but you have to tell git where the remote is
and which branch you want to use.

To **delete** a branch:

```
$ git branch -D deadend
```

To **delete a branch on a remote**:

```
$ git push :deadend
```


### **Pushing** your changes

When you are ready with your modifications you have to **push** the changes
back to your Github repository.

On a tracking branch it is simpe to push.

```
$ git push
```

On a non-tracking or from a tracking branch to a repository that is not the one
that you are tracking it's also not that hard. You just have to specify the
remote and the branch.

```
$ git push qLib-bess dev-0.2
```


### Sending a **Pull Request**

You can't push to every repository on Github. You have to have proper
permissions to do that. But you can inform the maintainers of other
repositories that you think you have something that they may pull by sending
pull requests.

Press the Pull Request (the singular one with no 's' at the end) button next to
your repository name on Github. Select the source and the target repo and branch,
and give a meaningful description of you request.


