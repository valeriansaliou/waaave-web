/*
 * Waaave Events
 * Logging wrapper
 *
 * Copyright 2014, Waaave
 * Author: Valerian Saliou <valerian@valeriansaliou.name>
 */


const NS = 'src/log';


// Instanciate the logging wrapper (configure loglevel)
exports.wrapper = function() {
    const log = require('loglevel');

    switch(process.env.NODE_ENV) {
        case 'production':
            log.setLevel('error');
            break;

        case 'testing':
            log.setLevel('info');
            break;

        default:
            log.setLevel('trace');
    }

    return log;
};
