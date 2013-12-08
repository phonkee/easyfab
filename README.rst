Easyfab
=======

Small wrapper around fabric.
This package is just a small project to have deployments right from the start
of development. It supports some callbacks so you can bring your own functionality.
Currently easyfab supports:

    * Virtualenv
    * Upgrade virtualenv on remote servers according to machine on which is project deployed
    * Multiple commands (django manage command, make_package, deploy)
    * packages are created to deployment/.packages directory so you will have history


Easyfab still under heavy development but api of custom Deployment will not be changed,
only added new functionality (new easyfabtasks).

Virtualenv
----------

easyfab needs virtualenv to work correctly on the remote server so please start
using it. For python programmers it's second best thing since sliced bread.

Installation:
-------------

via pip::
   
   $ pip install easyfab


or if you want latest version from repository, clone repository and run::

    $ python setup.py install


Usage:
------

in project top level directory simply run::

    $ easyfab init

Easyfab will generate fabfile.py which acts as proxy to easyfab. No need to edit it in the future.
Then if you want to add new deployment (in this case settings for production server)::

    $ easyfab add production

Now we can edit production deployment in deployment/production.py . easyfab makes
some sane defaults but there will be needed some changes.
Also there is directory deployment/production, where are generated skeleton
configurations for nginx, supervisor (more to come)

then you can simply run::

    $ fab use:production easyfab:deploy

and project will be **deployed** (nice huh?)

Built in commands
-----------------

Easyfab in current state provides this commands

    ``deploy``

    ``make_package``

    ``manage``

    ``upgrade_requirements``


More commands will come in future versions.

Custom commands
---------------

Every method on Deployment class which is decorated with ``@easyfabtask`` is task
and can be called from command line::

    $ fab use:production easyfab:my_custom_task

Also it supports arguments and keyword arguments (fabric does) so you can call::

    $ fab use:production easyfab:my_custom_task,argument1,argument2

Sources are templates
---------------------

Files with extensions defined in ``Deployment.processed_extensions`` will be
run through templating system (jinja2) with data context given in ``get_context_data`` method.
If you want you can add custom data override
``Deployment.get_context_data`` add custom data you want to use in your source
files and you are ready to go.

for example::

    def get_context_data(self, **kwargs):
        kwargs['version'] = '1.2.3b'
        super(Deployment, self).get_context_data(**kwargs)

Then simply you can add to your files ``{< version >}`` and you're done.
Template engine start and end tags are ``{< variable >}`` so it won't collide
with your template engine.

Items and get_item method
-------------------------

The most used method in Deployment class will be get_items.
These method should return list of ``items`` which easyfab will process.
Available items are

**CreateDirItem**

    this item creates directory. Arguments are

        ``directory_name`` - if this is absolute path it will be added to package_root directory

        e.g. ``/var/log/my_awesome_app`` will be added here ``.packaging/app-master/var/log/my_awesome_app``

**CopyItem**

    this item copies directory tree. Arguments are

        ``src`` - source. In case of relative path it will be used as child to ``project_dir``

        ``destination`` - In case of relative path it will be used as child to ``package_project_dir``

**SymlinkItem**

    this item makes symlinks. Arguments are

        ``src`` - source (existing file), If it's relative path, it will be a child to ``target_dir``

        ``destination`` - symlink location, If it's relative path it will be a child to ``package_project_dir`` otherwise it will be child to ``package_root``


Callbacks
---------

In case of any custom processing to package source files, you can use multiple callbacks

**pre_make_package**

    This callback will be called before make package is run, argument is context dictionary with all needed paths.
    You can run here e.g. ``compilemessages``, ``collectstatic``

**post_make_package**

    This callback will be called after make package is run (but before actual gzipping), argument is context dictionary with all needed paths.
    You can run here commands that will process all copied files e.g. compression of javascript, css, etc..

Have phun.
