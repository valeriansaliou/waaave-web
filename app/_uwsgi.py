#!/bin/sh
''''exec python2 -- "$0" ${1+"$@"} # '''

import os, sys


os.chdir(os.path.join(os.path.dirname(__file__), '../'))

args = sys.argv[1:] if len(sys.argv) > 1 else []
return_code = 1 if os.system('. ./env/bin/activate; ./env/bin/uwsgi --chdir ./app/ --wsgi-file ./_core/wsgi.py %s' % ' '.join(args)) else 0

sys.exit(return_code)