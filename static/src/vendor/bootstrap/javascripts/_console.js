var Console = (function () {

  var self = {};


  /* Variables */
  self._development = $('html').attr('data-environment') == 'development';
  self._available = typeof(window.console) != 'undefined';
  self._has = self._development && self._available;
  self._console = self._available ? console : {};


  /* Adapters */
  self._adapter = function (level) {
    if (!self._has) {
      return function() {}
    }

    var adapter = null;
    try {
      switch (level) {
        case 0:
          adapter = console.warn; break;
        case 1:
          adapter = console.error; break;
        case 2:
          adapter = console.info; break;
        case 3:
          adapter = console.log; break;
        case 4:
          adapter = console.debug; break;
      }
    } catch (e) {
      adapter = function() {}
    }

    return adapter.bind(self._console);
  }


  /* Methods */
  self.warn = self._adapter(0);
  self.error = self._adapter(1);
  self.info = self._adapter(2);
  self.log = self._adapter(3);
  self.debug = self._adapter(4);


  return self;

})();