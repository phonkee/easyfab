#
# Base deployment class
#
# @author phonkee@phonkee.eu
#

from fabric.api import cd, local, lcd, puts, run, sudo, put
from fabric.colors import green, red, magenta
from unipath import Path
from .api import virtualenv
from .errors import GitError
from .decorators import easyfabtask
from .items import BaseItem
from .utils import process_directory, get_relative_path, get_project_name

import inspect

class BaseDeployment(object):
    """ BaseDeployment class
        contains building blocks for deployments etc..
    """

    deployment = None
    deployment_files_dir = None
    packaging_dir = None
    project_dir = None
    virtualenv_dir = None
    mode = 0777

    def __init__(self, deployment, project_dir, deployment_dir):
        self.deployment = deployment
        self.project_dir = Path(project_dir)
        self.deployment_dir = Path(deployment_dir)
        self.packages_dir = self.deployment_dir.child('.packages')
        self.target_dir = Path(self.target_dir)
        self.deployment_files_dir = deployment_dir.child(deployment)

    @property
    def project_name(self):
	return get_project_name(self.project_dir)

    def get_package_name(self):
        """ Returns package name (based on git revision, branch, deployment)
        """
        branch_identifier = 'on branch'
        result = local('git status', capture=True)
        for line in result.splitlines():
            index = line.lower().find(branch_identifier)
            if index >= 0:
                branch = line[index + len(branch_identifier):].strip()
                break
        else:
            raise GitError('Cannot identify branch from git.')
        try:
            result = local('git --no-pager log --max-count=1', capture=True)
        except:
            raise GitError('Cannot identify last revision from git.')
        revision = result.splitlines()[0].split()[1][:7]
        package_name = u'%s-%s-%s' % (self.deployment, branch, revision)
        return package_name

    @easyfabtask
    def deploy(self, force_make_package=False, **options):
        """ Deploy task
            Performs deployment
                1. makes package (calls pre, post methods)
                2. copy to server
                3. unpack on server
        """
        self.log('Running `pre_deploy`.')
        self.pre_deploy()

        package = self.make_package(**options)
        put(package, '/tmp', use_sudo=True)
        with cd('/tmp'):
            sudo('mkdir -p %s' % self.target_dir)
            sudo('tar zxf %s -C /' % package.name)
            sudo('rm %s' % package.name)

        self.log('Running `post_deploy`.')
        self.post_deploy()

    @easyfabtask
    def make_package(self, force_make_package=True, **options):
        """ Creates package to deployment/.packages/
        """
        def copy_files(context):
            # copy files from deployments
            if context['deployment_files_dir'].exists() and context['deployment_files_dir'].isdir():
                for i in context['deployment_files_dir'].walk():
                    rel_path = get_relative_path(i, context['deployment_files_dir'])
                    target = Path(context['package_project_dir'], rel_path)

                    if i.isdir():
                        target.mkdir(parents=True, mode=self.mode)
                    elif i.isfile():
                        local('cp -R %(i)s %(target)s' % locals())

        def pack_package(context):
            with lcd(context['package_root']):
                command = 'tar -zcf %(package_file)s *' % context
                local(command)
                command = 'mv %(package_file)s ../' % context
                local(command)
            context['package_root'].rmtree()

        package_name = self.get_package_name()
        package_root = self.packages_dir.child(package_name)
        package_file = "%s.tar.gz" % package_name
        full_package_file = self.packages_dir.child(package_file)
        if full_package_file.exists() and not force_make_package:
            return full_package_file

        if package_root.exists() or package_root.isdir():
            package_root.rmtree()
            puts('Package directory `%s` exists, removing.' % package_root)

        self.log('Creating package directory `%s`.' % package_root)

        package_root.mkdir(parents=True, mode=self.mode)

        package_project_dir = package_root.child(*self.target_dir.components()[1:])
        package_project_dir.mkdir(parents=True, mode=self.mode)

        context = self.get_context_data(
            package_root=package_root,
            package_project_dir=package_project_dir,
            package_file=package_file,
            package_name=package_name
        )

        # run pre_make_package
        if callable(getattr(self, 'pre_make_package', None)):
            self.log('Running `pre_make_package`.')
            self.pre_make_package(context, **options)

        # copy files from deployment directory
        copy_files(context)

        # process all items
        for item in self.get_items(context, **options):
            if isinstance(item, BaseItem):
                item.run(context)
            else:
                self.log("Don't what to do with %s" % item)

        self.log('Post processing package')

        # post process package directory
        process_directory(context['package_root'], context,
                          extensions=self.processed_extensions)

        # call post_make package
        if callable(getattr(self, 'post_make_package', None)):
            self.log('Running `post_make_package`.')
            self.post_make_package(context, **options)

        self.log('Packing package.')
        pack_package(context)

        return full_package_file

    @easyfabtask
    def manage(self, arg):
        """ Runs manage.py command on remote hosts
        """
        full_manage_dir = Path(self.target_dir, Path(self.manage_dir))
        with virtualenv(str(self.virtualenv_dir), full_manage_dir):
            sudo('manage.py %s' % arg)

    @easyfabtask
    def upgrade_requirements(self):
        """ Freezes pip installed packages and upgrades them on server
        """
        local('pip freeze > /tmp/requirements.txt')
        put('/tmp/requirements.txt', '/tmp')

        with virtualenv(str(self.virtualenv_dir), '/tmp'):
            run('pip install -r requirements.txt')

    @easyfabtask
    def list_commands(self):
        """ Returns list of available easyfab commands for current deployment
        """
        for i in dir(self):
            attr = getattr(self, i)
            if not callable(attr):
                continue
            if getattr(attr, '__easyfabtask', None):
                if attr.__doc__:
                    doc = attr.__doc__.strip()
                else:
                    doc = None
                result = {
                    'name': attr.__name__,
                    'doc': doc,
                    'args': None
                }

                argspec = inspect.getargspec(attr)
                if argspec.args:
                    result['args'] = argspec.args

                print red(result['name'])
                if result['doc']:
                    print "\t" + result['doc']
                if result['args']:
                    print magenta('args:' + str(result['args']))

    def pre_deploy(self):
        """ Callback called before deploy, best place to run compilemessages,
            collectstatic and other commands
        """

    def post_deploy(self):
        """ Callback called before deploy, best place to run compilemessages,
            collectstatic and other commands
        """

    def log(self, message, level='INFO'):
        puts(green('easyfab:') + (" ".join((level, message))))

    def get_context_data(self, **kwargs):
        """ returns data to be added to deployment, after make package
            this is place where you can add your custom variables to be processed
            in source code e.g. version in source {< version >}
        """
        kwargs['packages_dir'] = Path(self.packages_dir)
        kwargs['project_dir'] = Path(self.project_dir)
        kwargs['project_name'] = self.project_name
        kwargs['virtualenv_dir'] = Path(self.virtualenv_dir)
        kwargs['target_dir'] = Path(self.target_dir)
        kwargs['deployment_dir'] = Path(self.deployment_dir)
        kwargs['deployment_files_dir'] = Path(self.deployment_files_dir)
        return kwargs
