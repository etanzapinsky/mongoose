import os

from fabric.api import local, lcd

def clean():
    print 'in dir: .'
    local('rm -rf *.pyc *~ parser.out parsetab.py')
    for dirpath, dirnames, filenames in os.walk('.'):
        if '.git' in dirnames:
            # dont go into any .git directories
            dirnames.remove('.git')
        if dirnames != []:
            for dirname in dirnames:
                with lcd(dirname):
                    print 'in dir: %s' % dirname
                    local('rm -rf *.pyc *~')
