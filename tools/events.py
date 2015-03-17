#!/bin/sh
''''exec python2 -- "$0" ${1+"$@"} # '''

import os, sys


os.chdir(os.path.join(os.path.dirname(__file__), '../'))

args = dict(
    map(
        lambda x: x.lstrip('-').split('='),
        sys.argv[1:]
    )
)

return_code = 1

if 'env' in args:
    command_base = 'export NODE_ENV={env}; ./events/run.js {args}'

    if 'logfile' in args:
        logfile = args['logfile']
        command_base = '%s >>{logfile} 2>&1' % command_base
    else:
        logfile = None

    args_recompose = [
        '--%s=%s' % (arg, value)
        for arg, value in args.items()
        if arg not in ('env', 'logfile')
    ]

    command_exec = command_base.format(
        env=args['env'],
        args=' '.join(args_recompose),
        logfile=logfile
    )

    return_code = 1 if os.system(command_exec) else 0
else:
    print('Please provide the environment in which to run the eventing server (env)')

sys.exit(return_code)
