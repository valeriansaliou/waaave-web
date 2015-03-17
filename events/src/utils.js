/*
 * Waaave Events
 * Utilities
 *
 * Copyright 2014, Waaave
 * Author: Valerian Saliou <valerian@valeriansaliou.name>
 */


const NS = 'src/utils';

const log = require('./log').wrapper();


// Check if an object has missing arguments
exports.has_all_keys = function(object, required_args) {
    var all_keys = true;

    for(var a in required_args) {
        if(object[required_args[a]] === undefined) {
            all_keys = false;
            break;
        }
    }

    return all_keys;
};
