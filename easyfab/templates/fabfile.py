"""
Universal deployment file based on fabric generated at {{ datetime }}
"""

import easyfab as ef
import fabric.api
import traceback
import unipath
import inspect

PROJECT_DIR = unipath.Path(__file__).parent


@fabric.api.task
def use(deployment):
    try:
        ef.set_deployment(PROJECT_DIR, deployment)
    except ef.MissingDeploymentError:
        return fabric.api.abort("Deployment %s does not exist" % deployment)


@fabric.api.task
@ef.ensure_use_deployment
def easyfab(name, *args, **kwargs):
    deployment = fabric.api.env['__deployment']

    func = getattr(deployment, name, None)
    if not func or not callable(func):
        fabric.api.abort("Easyfab command `%s` not found on deployment %s" % (name, inspect.getfile(deployment.__class__)))

    if ef.is_easyfab_task(func):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print traceback.format_exc()
            fabric.api.abort("Command %s raised exception %s" % (name, e))
    else:
        fabric.api.abort("Command %s is not an easyfab task" % name)
