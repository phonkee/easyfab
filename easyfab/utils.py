from jinja2 import Environment, FileSystemLoader
from .errors import MissingDeploymentError

from unipath import Path, FILES_NO_LINKS

import importlib
import sys


def get_rendered_template(filename, context, templates_dir='templates',
                          variable_start_string='{{', variable_end_string='}}'):
    """ Renders template
    """
    full_templates_dir = Path(__file__).parent.child(templates_dir)
    jinja_env = Environment(loader=FileSystemLoader(full_templates_dir),
                            variable_start_string=variable_start_string,
                            variable_end_string=variable_end_string)
    return jinja_env.get_template(filename).render(**context)


def get_deployment_info(directory, name, deployment_dir='deployment'):
    d = Path(directory).child(deployment_dir).child(name)
    f = Path(directory).child(deployment_dir).child("%s.py" % name)
    return d, f


def get_deployment_class(directory, name):
    """ Returns deployment class
    """
    dd, df = get_deployment_info(directory, name)
    deployment_dir = df.parent
    sys.path.insert(0, str(deployment_dir))
    try:
        module = importlib.import_module(name)
    except ImportError:
        raise MissingDeploymentError()
    return getattr(module, 'Deployment')


def get_project_name(directory):
    p = Path(directory)
    return str(p.components()[-1])


def is_easyfab_task(func):
    """ TODO: find out how to handle stacked decorators
    """
    return True


def process_directory(directory, context, variable_start_string='{<',
                      variable_end_string='>}', extensions=None,
                      filter=FILES_NO_LINKS):
    directory = Path(directory)

    for f in directory.walk(filter=filter):
        if extensions:
            if f.ext not in extensions:
                continue

        components = f.components()
        td, tf = Path(*components[:-1]), components[-1]

        jinja_env = Environment(loader=FileSystemLoader(str(td)),
                                variable_start_string=variable_start_string,
                                variable_end_string=variable_end_string,
                                block_start_string='{<%',
                                block_end_string='%>}',
                                comment_start_string='{<#',
                                comment_end_string='#>}',
                                )
        try:
            rendered = jinja_env.get_template(str(tf)).render(**context)
        except Exception, e:
            print "Cannot process file %s on line %s" % (
                e.filename,
                e.lineno
            )
            continue
        f.write_file(rendered.encode('utf-8'))


def get_relative_path(path, parent_path):
    return Path(Path(parent_path).rel_path_to(path))


def strip_root(path):
    return path.split_root()[1]
