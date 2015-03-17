#!/bin/sh
''''exec python2 -- "$0" ${1+"$@"} # '''

################
#### MANAGE ####
################

# Note: used for development to launch Django operations
# Settings are changed in Django website settings

import os, sys

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass 


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
