#!/bin/sh
# -*- coding: utf-8 -*- 
''''exec python2 -u -- "$0" ${1+"$@"} # '''

##############
#### TEST ####
##############

# Note: used for development to launch Unit tests
# Mostly called by a GitLab CI Runner instance

import os, sys


# Go to project root
os.chdir(os.path.join(os.path.dirname(__file__), '../'))


def init_environment(env):
    f_env = open('./app/_settings/environment.py','w+')
    f_env.write('import os\n')
    f_env.write('os.environ["DJANGO_ENVIRONMENT"] = "%s"' % env.replace('"', '\\"'))
    f_env.close()

    f_env = open('./app/_settings/local.py','w+')
    f_env.write('SITE_ID = 1')
    f_env.close()


# Load testing environment?
if len(sys.argv) > 1 and sys.argv[1] == 'testing':
    os.environ['DJANGO_ENVIRONMENT'] = 'testing'
    init_environment('testing')

import _settings


# Setup environment
init_environment(_settings.ENVIRONMENT)


# Run tests
module_ns = "test"
trace_code = ""
return_code = 0

tests = [
    ["deploy", [
        ["all", "./tools/deploy.py"],
    ]],

    ["django", [
        ["check", "./tools/manage.py check"],
        ["validate", "./tools/manage.py validate"],
        ["test", "./tools/manage.py test %s" % " ".join(_settings.INSTALLED_APPS_WAAAVE_INTERNAL)],
        ["kill", "./tools/run.py kill"],
    ]],

    ["events", [
        ["lint", "cd ./events; npm run-script lint"],
    ]],

    ["static", [
        ["lint", "cd ./static; npm run-script lint"],
    ]],
]

for cur_test in tests:
    cur_test_name = cur_test[0]

    for cur_test_task in cur_test[1]:
        cur_test_code = 0
        cur_test_ns = "%s:%s" % (cur_test_name,cur_test_task[0],)

        print("--(%s)[RUN:%s]--" % (module_ns,cur_test_ns,))
        cur_test_code = os.system(cur_test_task[1])
        print("--(%s)[DONE:%s]--\n" % (module_ns,cur_test_ns,))

        if cur_test_code is not 0:
            return_code = 1

        trace_code += "--(%s)[STATUS:%s:%s → %s]--\n" % (module_ns,cur_test_name,cur_test_task[0],cur_test_code,)

print(trace_code)

print("Test done (environment: %s)" % _settings.ENVIRONMENT)


# Exit with proper return code
sys.exit(return_code)