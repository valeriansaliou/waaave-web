#!/usr/bin/env node

/*
 * Waaave Events
 * Eventing server (uses Socket.IO)
 *
 * Copyright 2014, Waaave
 * Author: Valerian Saliou <valerian@valeriansaliou.name>
 */


const NS = 'run';
const _FN = '[' + NS + ']';


// Imports
const http_handler = require('./src/http_handler');
const django_api = require('./src/django_api');
const utils = require('./src/utils');
const log = require('./src/log').wrapper();
const fs = require('fs');


// Read arguments
const command_arguments = require('minimist')(process.argv.slice(2));
const required_args = [
    'redis_host', 'redis_port', 'redis_db', 'api_url', 'api_key'
];

if(utils.has_all_keys(command_arguments, required_args) === false) {
    console.error(_FN, 'Missing command arguments, not starting. Bye.');

    process.exit(1);
}

if(!command_arguments.socket && !command_arguments.port) {
    console.error(_FN, 'Please specify a socket or port argument. Not starting. Bye.');

    process.exit(1);
}

if((command_arguments.port && isNaN(command_arguments.port)) || isNaN(command_arguments.redis_port)) {
    console.error(_FN, 'The port argument must be numbers. Not starting. Bye.');

    process.exit(1);
}


// Cleanup UNIX socket (NodeJS won't bind if socket file already exists)
if(command_arguments.socket && fs.existsSync(command_arguments.socket)) {
    fs.unlink(command_arguments.socket);
}


// Globals
var SESSION_CACHE = {};
const API_URL = command_arguments.api_url;
const API_KEY = command_arguments.api_key;
const ENVIRONMENT = process.env.NODE_ENV || 'development';
const DEBUG = (ENVIRONMENT !== 'production');


console.info('Starting Waaave Events @' + ENVIRONMENT + ':DEBUG(' + DEBUG + ')');


// Configure HTTP server
const server = require('http').createServer(function(request, response) {
    http_handler.handle(ENVIRONMENT, request, response);
}).listen(command_arguments.socket || command_arguments.port);

const io = require('socket.io').listen(server);


// Configure Redis broker
const redis = require('socket.io/node_modules/redis');

const redis_sub = redis.createClient(
    command_arguments.redis_port,
    command_arguments.redis_host
);
redis_sub.select(command_arguments.redis_db);

redis_sub.subscribe('public');
redis_sub.subscribe('private');


// Socket.IO configuration
io.configure('development', function() {
    io.set('log level', 2);

    io.set('transports', [
        'xhr-polling'
    ]);
});

io.configure('testing', function() {
    io.set('log level', 2);

    io.set('transports', [
        'websocket',
        'xhr-polling',
        'jsonp-polling'
    ]);
});

io.configure('production', function() {
    io.enable('browser client etag');
    io.enable('browser client gzip');

    io.set('log level', 0);

    io.set('transports', [
        'websocket',
        'xhr-polling',
        'jsonp-polling'
    ]);
});


// Socket.IO authentication wrapper
io.set('authorization', function(handshake, accept) {
    const FN = '[' + NS + '.io:authorization' + ']';

    const session_key = handshake.query.session_key;

    if(session_key) {
        const user_id = django_api.read_user_id(session_key, SESSION_CACHE, {
            url: API_URL,
            key: API_KEY
        });

        log.debug(FN, SESSION_CACHE);

        if(user_id) {
            return accept(null, true);
        } else {
            return accept('Unknown session key.', false);
        }
    } else {
        return accept('No session key transmitted.', false);
    }
});


// Socket.IO handler
io.sockets.on('connection', function(socket) {
    const FN = '[' + NS + '.io:connection' + ']';

    // Read user ID from session cache
    // User ID should have been retrieved previously while authenticating
    const session_key = socket.handshake.query.session_key;

    if(session_key) {
        var user_id = SESSION_CACHE[session_key];

        if(user_id) {
            user_id = user_id + '';

            // Grab message from Redis and send to client
            redis_sub.on('message', function(channel, payload) {
                try {
                    log.debug(FN, payload);

                    payload = JSON.parse(payload);
                    const payload_user = payload.auth.user + '';

                    if(typeof payload.auth == 'object' && payload.data) {
                        // User not allowed to receive this payload
                        if(payload.auth.has && (user_id === null || !payload_user || payload_user != user_id)) {
                            return;
                        }

                        socket.emit(channel, payload.data);

                        log.debug(FN + ' >> ' + channel, payload.data);
                    }
                } catch(e) {
                    log.error(FN, e);
                }
            });
        }
    }
});


// Uncaught exceptions handler
if(DEBUG === false) {
    const gitlab = require('gitlab-logging');

    const gitlab_required_args = [
        'gitlab_token', 'gitlab_host', 'gitlab_project_id', 'gitlab_assignee_id'
    ];

    const GITLAB_ENABLED = utils.has_all_keys(command_arguments, gitlab_required_args);

    gitlab.configure({
        token: command_arguments.gitlab_token,
        host: command_arguments.gitlab_host,
        project_id: command_arguments.gitlab_project_id,
        assignee_id: command_arguments.gitlab_assignee_id,
        environment: ENVIRONMENT
    });

    // Prevents NodeJS to display a traceback when receiving too many requests
    process.setMaxListeners(0);

    process.on('uncaughtException', function(error) {
        const FN = '[' + NS + '.process:uncaught_exception' + ']';

        const error_stack = error.stack || error;
        log.error(FN, error_stack);

        // Open issue on GitLab (if defined)
        if(GITLAB_ENABLED === true) {
            gitlab.handle(error_stack);
        }
    });

    console.info('Will report uncaught exceptions to GitLab, you\'re in good hands.');
}
