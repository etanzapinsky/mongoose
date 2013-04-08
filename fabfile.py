import os

from fabric.api import local, lcd

def clean():
    print 'in dir: .'
    local('rm -rf *.pyc *~')
    for dirpath, dirnames, filenames in os.walk('.'):
        if '.git' in dirpath:
            # dont go into any .git directories
            # dirnames.remove('.git')
            pass
        if not dirpath or not '.git' in dirpath:
            with lcd(dirpath):
                print 'in dir: %s' % dirpath
                local('rm -rf *.pyc *~')
