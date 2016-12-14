# Deployment for project {{ project_name }}
# generated at {{ datetime }}

from easyfab import BaseDeployment
from easyfab import items


class Deployment(BaseDeployment):
    # list of all hosts
    hosts = ('127.0.0.1',)

    # all management tasks will be running on this host only
    master_host = '127.0.0.1'

    # target directory on remote servers
    target_dir = '/www/{{ project_name }}/'

    # remote directory where manage.py is located (relative to project dir)
    manage_dir = 'src/{{ project_name }}/'

    # local directory where manage.py is located (relative to project dir)
    local_manage_dir = 'src/{{ project_name }}/'

    # path to target virtualenv
    virtualenv_dir = '/www/virtualenv/{{ project_name }}'

    # which files will be processed as templates
    processed_extensions = ['.py', '.html', '.conf']

    def get_items(self, context, **options):
        """ You have to yield items
            from easyfab.items
        """
        # create directories
        # CreateDirItem argument is directory to be created
        #   if this is relative path, it will be added to package project directory
        #   if this is absolute path, it will be added to package root path
        yield items.CreateDirItem('log')
        yield items.CreateDirItem('conf')
        yield items.CreateDirItem('static')
        yield items.CreateDirItem('media')

        # CopyItem copies directory
        #   arguments are: source, destination
        #       if source is relative path, it will be child of project path,
        #           otherwise root of system will be used

        # yield items.CopyItem(
        #    'src/{{ project_name }}', context['package_project_dir'].child('src')
        # )

        # SymlinkItem
        #   creates symbolic link
        #       arguments are: source, destination (symlink)
        #           source: if relative - it will be child of target_dir
        #           destination: if absolute - absolute path on the remote server
        #                        if relative - package project dir will be parent of it

        # yield items.SymlinkItem(
        #    'conf/supervisor.conf',
        #    '/etc/supervisor/conf.d/{{ project_name }}.conf'
        # )
        # yield items.SymlinkItem(
        #    'conf/nginx.conf',
        #    '/etc/nginx/conf.d/{{ project_name }}.conf'
        # )

        # def pre_make_package(self, context, **options):
        #    """ Callback called after package directory has been created
        #       :context: - context is dictionary with all needed paths
        #                   all paths will be instance of unipath.Path so no need
        #                   to run os.path.join, etc.. You can use real power of unipath
        #       :options: are options passed to make_package (deploy)
        #    """
        #    with fabric.api.settings(warn_only=True):
        #        with fabric.api.lcd(self.local_manage_dir):
        #            fabric.api.local('./manage.py collectstatic --noinput --clear')
        #            fabric.api.local('./manage.py compilemessages')

        # def post_make_package(self, context, **options):
        #    """ Callback called after package directory has been created
        #       :context: - context is dictionary with all needed paths
        #                   all paths will be instance of unipath.Path so no need
        #                   to run os.path.join, etc.. You can use real power of unipath
        #       :options: are options passed to make_package (deploy)
        #    """
        #    self.log('nice to meet you post_make_package callback')

        # def get_context_data(self, **kwargs):
        #    """ Here you can add custom variables for processing package source code
        #    """
        #    return super(Deployment, self).get_context_data(**kwargs)
