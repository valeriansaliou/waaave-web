// Extend jQuery.fn with our new method
jQuery.extend(jQuery.fn, {
    // Name of our method & one argument (the parent selector)
    hasParent: function(p) {
        // Returns a subset of items using jQuery.filter
        return this.filter(function() {
            // Return truthy/falsey based on presence of parent in upward tree
            return $(this).parents(p).size();
        });
    }
});