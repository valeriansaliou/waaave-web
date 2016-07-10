Waaave - Installation Instructions
==================================

**This file contains the installation instruction of the Waaave development environment.**

*Waaave is composed of 4 completely isolated dynamic environments that are the Django app (located in app/), the Events (located in events/), the Statics (located in static/) and the Medias (located in media/). The other main folders (template/ for instance) don't require any particular setup.*

## Requirements Setup Guide

Some parts of this tutorial will require you to have Homebrew available (via the *brew* command).

Simply copy and paste this command to install it:

> ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"

If the command does not work, give a look to http://brew.sh/ to get latest installation instructions.

You may also need to install Xcode Command Line Tools (used for compiling latter sources):

> xcode-select --install

A prompt window will open, just follow the installation step.

## Django Setup Guide

This guide will help you get Waaave running on your local computer, thus so that you can develop on the top of it in good conditions.

This tutorial only covers MacOS systems with MAMP app. If your base system is different, give some Google searches and you'll find some good tuts.

### 1. Clone the Waaave code

In a terminal, go to your Web directory and execute the following command:

> git clone -b master git@github.com:valeriansaliou/waaave-web.git

Check you are currently using the master branch using:

> git branch

You should see something like: '* master'.

### 2. Configure MAMP

Now we need to properly configure MAMP to reproduce the final server conditions.

First of all, check that your MAMP environment **allows .htaccess files**, and that **mod_rewrite, mod_alias, mod_proxy and mod_proxy_http are enabled**.

Then, **create 5 hosts**, pointing to the given folder (make the path absolute):

* **waaave.com.dev** - ./public
* **avatar.waaave.com.dev** - ./avatar
* **events.waaave.com.dev** - ./events
* **static.waaave.com.dev** - ./static
* **media.waaave.com.dev** - ./media

The .htaccess files will do the rest (proxying, aliasing and so).

### 3. Install MySQL stuff

Now that Django is installed, we need a working Python connector to the MySQL DBMS. There's MySQLdb (aka mysql-python) which is very good at that job.

**Note: this part is very tricky. It involves a lot of commands, including compilation ones. While your computer will be working, go get a good coffee, you deserve it. Truly.**

#### Build MySQL sources

**Note: replace all the X.X.X in the MySQL files/folders commands below with the version of MySQL that you downloaded.**

1. Install CMake from: http://www.cmake.org/
2. Download MAMP Components from: http://sourceforge.net/projects/mamp/files/latest/download?source=files
3. Unpack the downloaded MAMP Components archive and only keep the mysql-X.X.X.tar.gz file
4. Execute the following commands (this can take a while):

> cd /usr/local
> sudo mv /path/to/mysql-X.X.X.tar.gz .
> tar xf mysql-X.X.X.tar.gz
> rm mysql-X.X.X.tar.gz
> mv mysql-X.X.X mysql
> cd mysql
> cmake . -DMYSQL_UNIX_ADDR=/Applications/MAMP/tmp/mysql/mysql.sock -DCMAKE_INSTALL_PREFIX=/Applications/MAMP/Library
> make -j  3
> cp libmysql/*.dylib /Applications/MAMP/Library/lib/
> mkdir -p /Applications/MAMP/Library/include/mysql
> cp -R include/* /Applications/MAMP/Library/include/mysql

*This help section was directly inspired from: http://blog.joynag.net/2012/04/using-mamp-mysql-installation-with-rails-app/*

### 4. Install dependencies

Waaave requires a few external dependencies, including libraries and backends to be running in background, mostly for fast storage purpose (high I/O).

#### a. Install Redis

Redis is a fast and reliable key-value storage backend, that Waaave uses to run asynchronous tasks in background (like sending emails on user action), or cache some random stuff.

**Install it using Homebrew:**

> brew install redis

Wait for the compilation and setup to finish, and Redis should be installed on your computer.

**Now, make it auto-start when your system boots up:**

> ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents
> launchctl load ~/Library/LaunchAgents/homebrew.mxcl.redis.plist

All done, Redis should now be started.

**Check its status by executing:**

> ps -ax | grep redis-server

**You should get an output like this:**

```bash
➜  ~  ps -ax | grep redis-server
29303 ??         0:00.13 /usr/local/opt/redis/bin/redis-server /usr/local/etc/redis.conf
29451 ttys006    0:00.00 grep redis-server
```

#### b. Install imaging libraries

Waaave use some advanced image manipulation techniques, which require you to setup JPEG and PNG libraries.

**Install them using Homebrew:**

> brew tap homebrew/dupes
> brew install libtiff libjpeg libpng zlib webp littlecms

### 5. Install Python stuff

Waaave is built on the top of Django, which must be installed on your system.

#### a. Install Python

Get Python 2.7 there: http://python.org/download/

Download the latest Python 2.7 MacOS 64 bits DMG file.

#### b. Install PIP

PIP is an excellent Python package manager, which allows you to seamlessly install any distributed Python module to your distribution, just as you would do with 'aptitude' on a Debian system.

We need it to install Django and further required Python packages. All in a snap.

Then, open a terminal and execute:

> curl http://python-distribute.org/distribute_setup.py | python2
> curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python2
> export PATH=/Library/Frameworks/Python.framework/Versions/2.7/bin:$PATH

Last command, assuming your Python version number is 2.7 (latest of 2.x branch).

Check for errors, if none, PIP is now installed!

**Note: the path export we did above is not definitive. Once you'll start a new shell it will be lost if not written in .bash_profile - so remember to do so!**

#### c. Install Virtualenv

To install Virtualenv (that wraps a Python virtual environment for our dependencies to work cleanly, separately from other Python apps), execute this:

> sudo pip install virtualenv

### 6. Configure the Waaave environment

Before we can start Waaave, we just need to tell it we're going to use it in the development mode. Which we call 'development' environment.

#### a. Environment name

In a terminal, go to the Waaave Web folder, and then execute:

> cd app/_settings/
> touch environment.py
> nano environment.py

Paste the following code in the freshly created file:

```python
import os

os.environ["DJANGO_ENVIRONMENT"] = "development"
```

Then, save pressing CTRL + O.

**Note: we asked you to create that file because it is not (and it SHOULD NEVER BE) present on the Git remote.**

#### b. Environment settings

If ever, you need to add your own Django settings or override the default ones from your current environment, put them in the following file:

> app/settings/local.py

**Important: never change a predefined configuration file (like development.py) if you know the configuration lines that are changed are only for your needs. Remember that any change in there is made global across all developers.**

### 7. Create databases

Open your MySQL admin tool (generally, PHPMyAdmin or SQLBuddy).

**Create the following empty database:**

* *waaave_development*

**Create the following MySQL user:**

* **Host**: *localhost*
* **User**: *waaave*
* **Password**: *(leave empty)*

**Assign the following database to the "waaave" user:**

* *waaave_development*


## Statics Setup Guide

Waaave uses smart tools to manage the way front-end developers work. This involves the use of SASS/Compass for stylesheets, as well as the GruntJS task automator for scripts (which is also used to call Compass and build everything in one command).

Let's install all that, step by step.

### 1. Install Compass

Compass is built upon the Ruby programming language. You first need to setup the Ruby interpreter and the Gems package manager.

#### a. Install Ruby

First, check that Ruby is not already installed on your system (it seems that on MacOS 10.8 it is already there, maybe that's just me).

Enter this in a terminal:

> ruby -v

If you don't get a line with the current Ruby version, you need to install Ruby, which you can get there: http://www.ruby-lang.org/en/downloads/

#### b. Install Gem

As with Ruby, Gem might be already there:

> gem -v

If not, go get it on: https://rubygems.org/pages/download

#### c. Install the Compass gem

Now that you got both Ruby and Gem to work, let's install Compass as a gem:

> sudo gem update --system
> sudo gem install compass

Test that Compass command can be called:

> compass -v

Nice, you got it running! Now, one last effort...

### 2. Install Grunt

Grunt is used to automate the whole process of static compilation (call to Compass, script minification/uglification and more).

It is written in JavaScript. Thus, it requires your system to have the NodeJS app.

#### a. Install NodeJS

Proceed the NodeJS setup:

> brew install node

Then test if both NodeJS and NPM are well installed:

> node -v
> npm -v

You shouldn't get any issue at this point. Otherwise, retry to install it or manually unlink/link it using Homebrew.

#### b. Install GruntJS

Now that you have both NodeJS and its package manager NPM available on your system, GruntJS can be installed in a snap:

> sudo npm install -g grunt-cli

Test the command now exists:

> grunt

You'll get an error from Grunt stating it could not find the Gruntfile. This is normal, it's telling us it's alive and working. That's good for now.

And... done!

### 3. Install the build dependencies

Before you can start using Grunt to compile the whole static set, you have to initialize the NodeJS components (on which this Grunt project depends) in the static/ directory.

Move to the Waaave Web's static/ directory and execute:

> npm install

NPM (Node Package Manager) will start to fetch the dependencies (defined in package.json), that are used in the statics build process. It should take 1 minute or so.

**Note: if ever, you see that a change is done in the package.json file, or that GruntJS does not want to work anymore, remove the node_modules/ directory and re-proceed this point.**


## Let's Deploy!

All the work here is automated, lucky you. Simply execute the few commands listed below and you'll get Waaave up and running.

### 1. Deploy Waaave

Now that all the requirements are satisfied, we can deploy Waaave.

Execute the following command:

> ./tools/deploy.py

This will configure some random stuff, build static files, fetch all dependencies and install them. And finally: start Waaave!

**Note: when something is not working fine after you pulled from Git, the reason might be that a dependency has been added or updated. The no-brainer solution to this is to re-run the deploy command above, again.**

### 2. Start Waaave

Whenever you want to start again the Waaave services, run the following command:

> ./tools/run.py

All done, it's now back running!

### 3. Stop Waaave

Whenever you want to stop all the Waaave services, execute:

> ./tools/run.py terminate

You can also use the *kill* command below (which is faster to execute, but does not exit gracefully the services - which can result in some loss of data):

> ./tools/run.py kill

So far, so good. Choose the compromise that best suits your needs depending on the situation in which you use this set of commands.


*Sounds good? Happy developing. You are now a Waaaver! :)*
