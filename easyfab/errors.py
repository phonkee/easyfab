class EasyfabError(Exception):
    """ Base for all errors
    """

class GitError(EasyfabError):
    pass


class MissingDeploymentError(EasyfabError):
    pass


class ExistingDeploymentError(EasyfabError):
    pass


class NonExistingDirectoryError(EasyfabError):
    pass
