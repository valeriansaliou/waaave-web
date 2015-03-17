var Tooltip = function (param_el_sel, param_msg_val, param_buttons, param_callback_close_fn, param_lock_close) {

  var self = this;


  /* Variables */

  /* @private */
  self._tooltip_id = TooltipID++;

  /* @private */
  self._tooltip_path = '.tooltip[data-id="' + self._tooltip_id + '"]';

  /* @private */
  self._tooltip_sel = null;

  /* @private */
  self._param_msg_val = param_msg_val;

  /* @private */
  self._param_el_sel = param_el_sel;

  /* @private */
  self._param_buttons = param_buttons;

  /* @private */
  self._param_callback_close_fn = param_callback_close_fn || function() {};

  /* @private */
  if(typeof param_lock_close === 'boolean') {
    self._param_lock_close = param_lock_close;
  } else {
    self._param_lock_close = false;
  }


  /* Helpers */

  /**
   * Generate the tooltip base HTML
   * @private
   * @return {undefined}
   */
  self._genHTML = function() {

    try {
      html =  '<span class="tooltip" data-id="%s">' + 
                  '<span class="tooltip-arrow"></span>' + 
                  '<span class="tooltip-content">' + 
                      '<span class="tooltip-text"></span>' + 
                      '<span class="tooltip-actions"></span>' + 
                  '</span>' + 
              '</span>';

      html = _.str.sprintf(html, self._tooltip_id);
      $('body').append(html);
    } catch(e) {
      Console.error('Tooltip._genHTML', e);
    }

  };

  /**
   * Append the tooltip text
   * @private
   * @return {undefined}
   */
  self._appendText = function() {

    try {
      self._tooltip_sel.find('.tooltip-text').text(self._param_msg_val);
    } catch(e) {
      Console.error('Tooltip._appendText', e);
    }

  };

  /**
   * Append the tooltip buttons
   * @private
   * @return {undefined}
   */
  self._appendButtons = function() {

    try {
      var tooltip_actions_sel = self._tooltip_sel.find('.tooltip-actions');
      var tooltip_btn_html = '';

      // Params
      for(i in self._param_buttons) {
        var cur_btn = self._param_buttons[i];

        // Assert
        if((!cur_btn[0] || typeof cur_btn[0] != 'string')   ||
           (typeof cur_btn[1] != 'string')                  ||
           (cur_btn[2] && typeof cur_btn[2] != 'function')) {
          Console.warn('Tooltip._appendButtons', 'Ignored an invalid button object.');
          continue;
        }

        // Build button DOM
        var cur_btn_text = cur_btn[0];
        var cur_btn_class = cur_btn[1] ? 'btn-' + cur_btn[1] : '';

        tooltip_btn_html += _.str.sprintf('<button class="btn btn-tiny %1s">%2s</button>', cur_btn_class, cur_btn_text);

        // Cleanup
        delete cur_btn;
        delete cur_btn_text, cur_btn_class;
      }

      // Add buttons to DOM
      tooltip_actions_sel.html(tooltip_btn_html);

      // Bind click events on buttons
      var tooltip_actions_btn_sel = tooltip_actions_sel.find('button');

      $.each(self._param_buttons, function(j, cur_btn_val) {
        tooltip_actions_btn_sel.eq(j).click(function() {
          try {
            if(cur_btn_val && cur_btn_val[2]         &&
               typeof cur_btn_val[2] == 'function')  {
              cur_btn_val[2]();
            }
          } catch(e) {
            Console.error('Tooltip._appendButtons[btn:click]', e);
          } finally {
            if(self._param_lock_close !== true) {
              self._destroy();
            }
            return false;
          }
        });
      });
    } catch(e) {
      Console.error('Tooltip._appendButtons', e);
    }

  };

  /**
   * Returns whether the tooltip is already opened or not
   * @private
   * @return {boolean}
   */
  self._isOpen = function() {

    try {
      var is_open = false;

      for(i in TooltipRegister) {
        if(TooltipRegister[i]._param_el_sel.is(self._param_el_sel)) {
          is_open = true; break;
        }
      }
    } catch(e) {
      Console.error('Tooltip._isOpen', e);
    } finally {
      return is_open;
    }

  };


  /* Methods (private) */

  /**
   * Initialize the tooltip
   * @private
   * @return {undefined}
   */
  self._init = function() {

    try {
      if(!self._isOpen()) {
        var init_is_clean = !self._destroyAll(self._init);

        if(init_is_clean) {
          self._register();
          self._build();
          self._events();
          self._reveal();
        } else {
          Console.info('Tooltip._init', _.str.sprintf('Destroying other tooltips before we can open tooltip #%s...', self._tooltip_id));
        }
      } else {
        Console.info('Tooltip._init', 'Tooltip already opened.');
      }
    } catch(e) {
      Console.error('Tooltip._init', e);
    }

  };

  /**
   * Register the tooltip
   * @private
   * @return {undefined}
   */
  self._register = function() {

    try {
      TooltipRegister[self._tooltip_id] = self;
    } catch(e) {
      Console.error('Tooltip._register', e);
    }

  };

  /**
   * Unregister the tooltip
   * @private
   * @return {undefined}
   */
  self._unregister = function() {

    try {
      delete TooltipRegister[self._tooltip_id];
    } catch(e) {
      Console.error('Tooltip._unregister', e);
    }

  };

  /**
   * Build the tooltip
   * @private
   * @return {undefined}
   */
  self._build = function() {

    try {
      // Initialize tooltip
      self._genHTML();
      self._tooltip_sel = $(self._tooltip_path);

      // Append tooltip contents
      self._appendText();
      self._appendButtons();
    } catch(e) {
      Console.error('Tooltip._build', e);
    }

  };

  /**
   * Attach the tooltip events
   * @private
   * @return {undefined}
   */
  self._events = function() {

    try {
      // Apply tooltip style + misc events
      self._position();
      self._autoHide();
      self._bindResize();
    } catch(e) {
      Console.error('Tooltip._events', e);
    }

  };

  /**
   * Bind the tooltip resize event
   * @private
   * @return {undefined}
   */
  self._bindResize = function() {

    try {
      $(window).bind('resize', self._position);
    } catch(e) {
      Console.error('Tooltip._bindResize', e);
    }

  };

  /**
   * Unbind the tooltip resize event
   * @private
   * @return {undefined}
   */
  self._unbindResize = function() {

    try {
      $(window).unbind('resize', self._position);
    } catch(e) {
      Console.error('Tooltip._unbindResize', e);
    }

  };

  /**
   * Attach the tooltip auto-hide event
   * @private
   * @return {undefined}
   */
  self._autoHide = function() {

    try {
      if(self._param_lock_close !== true) {
        $('body').on('click', function(evt) {
          try {
            var tg = $(evt.target);

            if(!(tg.parents().is(self._tooltip_sel)     ||
                 tg.is(self._tooltip_sel)               ||
                 tg.parents().is(self._param_el_sel)    ||
                 tg.is(self._param_el_sel)))            {
              self._destroy();
            }
          } catch(e) {
              Console.error('Tooltip._autoHide[body:click()]', e);
          }
        });
      } else {
        Console.info('Tooltip._autoHide', 'Tooltip auto-close is locked.');
      }
    } catch(e) {
      Console.error('Tooltip._autoHide', e);
    }

  };

  /**
   * Process & apply the tooltip position
   * @private
   * @return {undefined}
   */
  self._position = function() {

    try {
      // Read caller element position
      var el_pos = self._param_el_sel.offset();
      var el_width = parseInt(self._param_el_sel.outerWidth(), 10);
      var el_height = parseInt(self._param_el_sel.outerHeight(), 10);

      // Get tooltip element style
      var tooltip_width = parseInt(self._tooltip_sel.outerWidth(), 10);
      var tooltip_offset_top = 4;

      // Apply positions to tooltip
      self._tooltip_sel.css({
        'position': 'absolute',
        'z-index': 999999,
        'top': el_pos.top,
        'left': el_pos.left,
        'margin-top': el_height - tooltip_offset_top,
        'margin-left': -1 * (tooltip_width / 2) + (el_width / 2)
      });
    } catch(e) {
      Console.error('Tooltip._position', e);
    }

  };

  /**
   * Autofocus on the first tooltip button
   * @private
   * @return {undefined}
   */
  self._autofocus = function() {

    try {
      self._tooltip_sel.find('.tooltip-actions button:first').focus();
    } catch(e) {
      Console.error('Tooltip._autofocus', e);
    }

  };

  /**
   * Reveal the tooltip
   * @private
   * @return {undefined}
   */
  self._reveal = function() {

    try {
      self._tooltip_sel.hide().show('drop', {direction: 'up'}, 200, function() {
        self._autofocus();
      });
    } catch(e) {
      Console.error('Tooltip._reveal', e);
    }

  };

  /**
   * Destroy the tooltip
   * @private
   * @param {function} callback
   * @return {undefined}
   */
  self._destroy = function(callback) {

    try {
      if(self._param_lock_close !== true) {
        $('body').off('click');
      }

      self._tooltip_sel.hide('drop', {direction: 'down'}, 200, function() {
        self._tooltip_sel.remove();

        self._unbindResize();
        self._unregister();
        self._param_callback_close_fn();

        if(typeof callback == 'function') {
          callback();
        }
      });
    } catch(e) {
      Console.error('Tooltip._destroy', e);
    }

  };

  /**
   * Destroy all existing tooltips
   * @private
   * @param {function} callback
   * @return {boolean}
   */
  self._destroyAll = function(callback) {

    try {
      var count = 0;
      for(i in TooltipRegister) {
        if(++count === 1) {
          TooltipRegister[i]._destroy(function() {
            Console.info('Tooltip._destroyAll', _.str.sprintf('Other tooltips destroyed. Opening tooltip #%s now.', self._tooltip_id));
            callback();
          });
        } else {
          TooltipRegister[i]._destroy();
        }
      }
    } catch(e) {
      Console.error('Tooltip._destroyAll', e);
    } finally {
      return count;
    }

  };


  /* Assertions */
  if((!self._param_el_sel  || !self._param_el_sel.size()  || typeof self._param_el_sel  != 'object')  ||
     (!self._param_msg_val || typeof self._param_msg_val != 'string'                               )  ||
     (!self._param_buttons || !self._param_buttons.length || typeof self._param_buttons != 'object')) {
    return Console.error('Tooltip', 'Cannot initiate tooltip, invalid parameters.');
  }

  /* Initiation */
  self._init();

};

var TooltipID = 0;
var TooltipRegister = {};