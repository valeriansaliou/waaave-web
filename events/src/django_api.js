/*
 * Waaave Events
 * Django API helpers
 *
 * Copyright 2014, Waaave
 * Author: Valerian Saliou <valerian@valeriansaliou.name>
 */


const NS = 'src/django_api';

const log = require('./log').wrapper();

const querystring = require('querystring');
const url = require('url');
const http_sync = require('http-sync');


// Read user ID from Django API
exports.read_user_id = function(session_key, session_cache, api) {
    const FN = '[' + NS + '.read_user_id' + ']';

    var user_id = null;

    if(session_key) {
        log.debug(FN, 'Read user ID with session key: ' + session_key);

        if(typeof session_cache[session_key] != 'undefined') {
            log.debug(FN, 'Read user ID from session cache');

            user_id = session_cache[session_key];
        } else {
            log.debug(FN, 'Requesting user ID knowing the session ID...');

            // Proceed request
            var url_parse = url.parse(
                url.resolve(api.url, '/user/session/')
            );
            var protocol = url_parse.protocol.replace(':', '');
            var port = url_parse.port || (protocol == 'https' ? 443 : 80);

            var request = http_sync.request({
                method: 'POST',

                headers: {
                    'content-type' : 'application/x-www-form-urlencoded'
                },

                body: querystring.stringify({
                    'session_key': session_key,
                    'api_key': api.key
                }),

                protocol: protocol,
                host: url_parse.hostname,
                port: port,
                path: url_parse.pathname
            });

            // Timeout after 10 seconds
            var timedout = false;
            request.setTimeout(10000, function() {
                log.debug(FN, 'Request Timedout!');
                timedout = true;
            });

            var response = request.end();

            if(!timedout) {
                // Handle response
                try {
                    var body_string = response.body.toString();
                    var body = JSON.parse(body_string);

                    if(response.statusCode != 200) {
                        log.warn(FN, 'API replied: ' + body.message);
                        throw body.message;
                    } else {
                        user_id = body.contents.user_id;
                        session_cache[session_key] = user_id;

                        log.debug(FN, 'Got user ID from API: ' + user_id);
                    }
                } catch(e) {
                    log.error(FN, 'API response error: ' + e);
                }
            } else {
                log.warn(FN, 'API timed out');
            }
        }
    }

    return user_id;
};
