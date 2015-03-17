/*
 * Waaave Events
 * HTTP handlers
 *
 * Copyright 2014, Waaave
 * Author: Valerian Saliou <valerian@valeriansaliou.name>
 */


const NS = 'src/http_handler';

const log = require('./log').wrapper();


// HTTP server handler
exports.handle = function(environment, request, response) {
    const FN = '[' + NS + '.handle' + ']';

    const tag = '[waaave@' + environment + ']';
    const path = request.url || '/';
    const headers = {
        'Content-Type': 'text/plain; charset=UTF-8'
    };

    log.info(FN, 'Handle: ' + path);

    switch(path) {
        case '/':
        case '/index.html':
            response.writeHead(200, headers);
            response.end('Events Server ' + tag);
            break;

        case '/robots.txt':
            response.writeHead(200, headers);
            response.end('User-Agent: *\nDisallow: /\n');
            break;

        default:
            response.writeHead(404, headers);
            response.end('Not Found ' + tag);
    }
};
