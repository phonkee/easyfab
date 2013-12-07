from unipath import Path
import datetime
import fabric.api

from .errors import ExistingDeploymentError

from .utils import (get_deployment_class, get_deployment_info,
                    get_rendered_template, get_project_name
                    )


def init(directory, deployment_dir='deployment', mode=0777):
    """ Initializes easyfab fabric file along with deployments directory
    """
    directory = Path(directory)
    path = directory.child(deployment_dir)
    if path.exists():
        print 'Deployment directory already exists'
    else:
        path.mkdir(parents=True, mode=mode)

    # write module constuctor
    path.child('__init__.py').write_file("")

    fabfile = directory.child('fabfile.py')
    if fabfile.exists():
        print 'fabfile already exists'
    else:
        rendered = get_rendered_template('fabfile.py', {
            'datetime': datetime.datetime.now()
        })
        fabfile.write_file(rendered)


def add_deployment(directory, name, templates_dir='templates', deployment_dir='deployment', mode=0777):
    """ Adds new deployment if not exists
    """
    context = {
        'datetime': datetime.datetime.now(),
        'name': name,
        'project_name': get_project_name(directory)
    }

    dd, df = get_deployment_info(directory, name)

    if df.exists():
        raise ExistingDeploymentError()

    # create deployments directory
    df.parent.mkdir(parents=True, mode=mode)

    # write deployment file
    df.write_file(
        get_rendered_template('deployment.py', context)
    )
    top_td = Path(__file__).parent.child(templates_dir)
    td = top_td.child(deployment_dir)
    for tf in td.walk():
        if tf.isdir():
            continue
        partitioned = tf.partition(td)
        target = Path(dd, Path(partitioned[2][1:]))
        target_dir = target.parent
        if not target_dir.exists():
            target_dir.mkdir(parents=True, mode=mode)
        tmp = tf.partition(top_td)[2][1:]
        rendered = get_rendered_template(tmp, context)
        target.write_file(rendered)


def update_deployment(directory):
    """ TODO: update of deployment
    """
    pass


def set_deployment(directory, name):
    cls = get_deployment_class(directory, name)
    deployment_dir, _ = get_deployment_info(directory, name)
    project_dir = Path(directory)

    instance = cls(name, project_dir, Path(deployment_dir).parent)
    fabric.api.env['__deployment'] = instance
    fabric.api.env.hosts = instance.hosts

