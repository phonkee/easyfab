from contextlib import contextmanager as _contextmanager

import fabric.api


@_contextmanager
def virtualenv(virtualenv_directory, cd_directory=None):
    """ Context manager for running commands inside virtualenv
        cd_directory - if defined, we first change directory to it
    """
    if cd_directory:
        with fabric.api.cd(cd_directory):
            with fabric.api.prefix('source %s/bin/activate' % virtualenv_directory):
                yield
    else:
        with fabric.api.prefix('source %s/bin/activate' % virtualenv_directory):
            yield
