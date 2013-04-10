if [ $# -eq 0 ]
then
  which bpython >/dev/null 2>&1
  bpython_status=$?
  which ipython >/dev/null 2>&1
  ipython_status=$?
  if [ $bpython_status -eq 0 ]
  then
    PYTHONPATH='.' bpython $*
  elif [ $ipython_status -eq 0 ]
  then
    PYTHONPATH='.' ipython
  else
    PYTHONPATH='.' python $*
  fi
elif [ $1 = 'test' ]
then
  PYTHONPATH='.' nosetests
else
  PYTHONPATH='.' python $*
fi
