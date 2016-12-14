from unipath import Path
import fabric.api
from .utils import strip_root


class BaseItem(object):
    def run(self, context):
        raise NotImplementedError('Please implement run method on %s' % self.__class__.__name__)


class CreateDirItem(BaseItem):
    directory_name = None
    mode = None

    def __init__(self, directory_name, mode=0777):
        self.directory_name = Path(directory_name)
        self.mode = mode

    def run(self, context):
        if not self.directory_name.isabsolute():
            directory = Path(Path(context['package_project_dir']), self.directory_name)
        else:
            directory = Path(context['package_root'], Path(strip_root(self.directory_name)))

        directory.mkdir(parents=True, mode=self.mode)


class CopyItem(BaseItem):
    src = None
    destination = None
    only_content = None
    recursive = None

    def __init__(self, src, destination, only_content=False, recursive=False, follow_symlinks=True):
        self.follow_symlinks = follow_symlinks
        self.src = Path(src)
        self.destination = Path(destination)
        self.only_content = only_content
        self.recursive = recursive

    def run(self, context):
        if not self.src.isabsolute():
            self.src = Path(Path(context['project_dir']), self.src)
        if not self.destination.isabsolute():
            self.destination = Path(Path(context['package_project_dir']), self.destination)

        switches = []

        if self.recursive:
            switches.append("-R")

        if self.follow_symlinks:
            switches.append("-L")

        command = 'cp %(switches)s %(src)s %(destination)s' % {
            'switches': ' '.join(switches),
            'src': self.src,
            'destination': self.destination,
        }

        fabric.api.local(command, capture=True)


class SymlinkItem(BaseItem):
    src = None
    destination = None

    def __init__(self, src, destination):
        self.src = Path(src)
        self.destination = Path(destination)

    def run(self, context):
        if not self.src.isabsolute():
            self.src = Path(Path(context['target_dir']), self.src)

        if self.destination.isabsolute():
            destination = Path(context['package_root'], strip_root(self.destination))
        else:
            destination = Path(context['package_project_dir'], self.destination)

        parent_dir = destination.parent
        if not parent_dir.exists():
            parent_dir.mkdir(parents=True, mode=0777)

        command = 'ln -s %(src)s %(destination)s' % {
            'src': self.src,
            'destination': destination
        }
        fabric.api.local(command, capture=True)
