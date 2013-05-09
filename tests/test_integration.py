from nose.tools import *
import subprocess

def run_code_file(path):
    cmd = ['./manage.sh', 'mongoose.py', path]
    assert subprocess.call(cmd)
