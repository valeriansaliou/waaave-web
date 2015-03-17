#!/bin/sh
# -*- coding: utf-8 -*-
''''exec python2 -u -- "$0" ${1+"$@"} # '''

################
#### DEPLOY ####
################

# Note: used to automate deployment process
# Settings are changed in Django website settings

import sys, os, time, types
import _settings


# Go to project root
os.chdir(os.path.join(os.path.dirname(__file__), '../'))


# Start deployment
module_ns = "deploy"
trace_code = ""
return_code = 0

deploy_tasks = [
    ["static", [
        ["install", _settings.DEPLOY['static']['install']],
        ["clean", _settings.DEPLOY['static']['clean']],
        ["build", _settings.DEPLOY['static']['build']],
    ]],

    ["events", [
        ["install", _settings.DEPLOY['events']['install']],
    ]],

    ["django", [
        ["clean", _settings.DEPLOY['django']['clean']],
        ["env", _settings.DEPLOY['django']['env']],
        ["install", _settings.DEPLOY['django']['install']],
        ["syncdb", _settings.DEPLOY['django']['syncdb']],
        ["migrate", _settings.DEPLOY['django']['migrate']],
        ["index", _settings.DEPLOY['django']['index']],
        ["collectstatic", _settings.DEPLOY['django']['collectstatic']],
    ]],

    ["run", [
        ["stop", _settings.DEPLOY['run']['stop']],
        ["wait", (lambda: sys.stdout.write("Waiting...\n") and time.sleep(2)) if _settings.DEPLOY['run']['wait'] else ''],
        ["start", _settings.DEPLOY['run']['start']],
    ]],
]


for cur_deploy_task in deploy_tasks:
    cur_deploy_task_name = cur_deploy_task[0]

    for cur_deploy_task_task in cur_deploy_task[1]:
        if return_code is 0:
            cur_deploy_task_code = 0
            cur_deploy_task_ns = "%s:%s" % (cur_deploy_task_name,cur_deploy_task_task[0],)

            if cur_deploy_task_task[1]:
                print("--(%s)[RUN:%s]--" % (module_ns,cur_deploy_task_ns,))

                if isinstance(cur_deploy_task_task[1], str):
                    cur_deploy_task_code = os.system(cur_deploy_task_task[1])
                elif isinstance(cur_deploy_task_task[1], list):
                    cur_deploy_task_task_cmd = cur_deploy_task_task[1][0]
                    cur_deploy_task_task_params = cur_deploy_task_task[1][1] or []

                    cur_deploy_task_code = os.system(cur_deploy_task_task_cmd)

                    # Retry if packages setup error (sometimes happens...)
                    if cur_deploy_task_code > 0 and 'retry_error' in cur_deploy_task_task_params:
                        cur_deploy_task_code = os.system(cur_deploy_task_task_cmd)
                elif isinstance(cur_deploy_task_task[1], types.FunctionType):
                    cur_deploy_task_task[1]()

                print("--(%s)[DONE:%s]--\n" % (module_ns,cur_deploy_task_ns,))
            else:
                print("--(%s)[PASS:%s]--\n" % (module_ns,cur_deploy_task_ns,))

                cur_deploy_task_code = -1
        else:
            print("--(%s)[ABORT:%s]--\n" % (module_ns,cur_deploy_task_ns,))

            cur_deploy_task_code = -1

        if cur_deploy_task_code > 0:
            return_code = 1

        trace_code += "--(%s)[STATUS:%s:%s → %s]--\n" % (module_ns,cur_deploy_task_name,cur_deploy_task_task[0],cur_deploy_task_code,)

print(trace_code)

print("Deploy done (environment: %s)" % _settings.ENVIRONMENT)


# Exit with proper return code
sys.exit(return_code)