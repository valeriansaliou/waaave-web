// Bundle
var Utilities = (function () {

    /**
     * Alias of this
     * @private
     */
    var self = {};


    /**
     * Regex utilities
     * @public
     * @return {undefined}
     */
    self.Regex = new function() {

        /**
         * Alias of this
         * @private
         */
        var regex = this;


        /**
         * Regex utilities
         * @public
         * @param {string} raw_str
         * @return {string}
         */
        regex.escape = function(raw_str) {

            try {
                return raw_str.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
            } catch(e) {
                Console.error('Utilities.Regex.escape', e);
            }

        };

    };


    /**
     * Return class scope
     */
    return self;

})();


// Alias shortcut
var Util = Utilities;