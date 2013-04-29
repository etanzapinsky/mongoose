dyn-160-39-205-223:mongoose meirfischer$ cat ~/.bash_profile
export PATH="/usr/local/bin/python2.7:$PATH"
export PATH="/usr/local/share/python:$PATH"
source /usr/local/share/python/virtualenvwrapper.sh 

dyn-160-39-205-223:mongoose meirfischer$ cat ~/Envs/mongoose/bin/postactivate
#!/bin/bash
# This hook is run after this virtualenv is activated.
cd /Users/meirfischer/Dropbox/mongoose


