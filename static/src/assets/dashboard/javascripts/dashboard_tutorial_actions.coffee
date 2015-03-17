###
Bundle: Dashboard Tutorial Actions (assets)
Project: Waaave
Authors: Julien Le Coupanec, Valerian Saliou
Copyright: 2014, Hakuma Holdings Ltd.
###

__ = window



class DashboardTutorialActions
    init: ->
        try
            # Selectors
            @_tutorials_sel = $ '.tutorials'
            @_manager_form_sel = $ 'form.manager-form'
            @_tutorial_all_sel = @_tutorials_sel.find '.tutorial'
            @_tutorial_title_sel = @_tutorial_all_sel.find '.title'
            @_search_go_btn_sel = @_manager_form_sel.find 'button.search-tuto-submit'
            @_search_input_sel = @_manager_form_sel.find 'input.search-tuto-input'
            @_filter_all_sel = @_manager_form_sel.find '.filter'
            @_trash_btn_sel = @_manager_form_sel.find 'button.trash-button'
        catch error
            Console.error 'DashboardTutorialActions.init', error


    search_tutorial: ->
        try
            search_value = $.trim @_search_input_sel.val()

            if search_value
                value_regex_escaped = Util.Regex.escape search_value
                search_regex = new RegExp "(^| )(#{value_regex_escaped})", 'gi'

                tutorial_filter_sel = @_tutorial_all_sel
                filter_val = @_filter_all_sel.filter('.filter-active').attr 'data-val'

                if filter_val
                    tutorial_filter_sel = @_tutorial_all_sel.filter "[data-filter='#{filter_val}']"

                @_tutorial_all_sel.find('.title-search').remove()
                @_tutorial_title_sel.show()

                tutorial_filter_sel.hide()
                tutorial_filter_sel.filter( ->
                    return $(this).find('.tutorial-details .title a').text().match search_regex
                ).each( ->
                    cur_tutorial_sel = $ this

                    cur_tutorial_title = cur_tutorial_sel.find '.title'
                    cur_tutorial_title_search = cur_tutorial_title.clone().removeClass('title').addClass 'title-search'

                    cur_tutorial_title_search_val = cur_tutorial_title_search.find('a').text()
                    cur_tutorial_title_search_val = cur_tutorial_title_search_val.replace search_regex, '$1<span class="is-result">$2</span>'
                    cur_tutorial_title_search.find('a').html cur_tutorial_title_search_val

                    cur_tutorial_title.after cur_tutorial_title_search
                    cur_tutorial_title.hide()
                    cur_tutorial_sel.show()
                )
            else
                @_reset_search_tutorial()
        catch error
            Console.error 'DashboardTutorialActions.search_tutorial', error


    _reset_search_tutorial: ->
        try
            @_tutorial_all_sel.find('.title-search').remove()
            @_tutorial_title_sel.show()

            @_search_input_sel.val ''
            @_tutorial_all_sel.show()

            if typeof __.DashboardTutorialRoot.update_filter_tutorial is 'function'
                __.DashboardTutorialRoot.update_filter_tutorial()
        catch error
            Console.error 'DashboardTutorialActions._reset_search_tutorial', error


    event_search_tutorial: ->
        try
            self = @

            @_search_go_btn_sel.click -> self._search_tutorial()

            @_search_input_sel.keydown (e) ->
                switch e.keyCode
                    when 13
                        self._search_tutorial()
                        return false
                    when 27
                        self._reset_search_tutorial()
                        return false

            @_search_input_sel.typeWatch
                wait: 250
                captureLength: 0
                callback: -> self._search_tutorial.bind self
        catch error
            Console.error 'DashboardTutorialActions.event_search_tutorial', error


    _check_tutorial: (checkbox_sel, checkbox_all_sel) ->
        try
            self = @

            checkbox_checked_size = checkbox_all_sel.filter(':checked').size()

            if checkbox_checked_size is 1 and @_trash_btn_sel.is ':hidden'
                @_trash_btn_sel.show()
                @_trash_btn_sel.removeClass 'bounceOut animated'
                @_trash_btn_sel.addClass 'bounceIn animated'

                @_trash_btn_sel.stopTime()
                @_trash_btn_sel.oneTime(
                    '1s',
                    -> self._trash_btn_sel.removeClass 'bounceIn animated'
                )
            else if checkbox_checked_size is 0
                @_trash_btn_sel.removeClass 'bounceIn animated'
                @_trash_btn_sel.addClass 'bounceOut animated'

                @_trash_btn_sel.stopTime()
                @_trash_btn_sel.oneTime(
                    '1s',
                    ->
                        self._trash_btn_sel.removeClass 'bounceOut animated'
                        self._trash_btn_sel.hide()
                )
        catch error
            Console.error 'DashboardTutorialActions._check_tutorial', error


    event_check_tutorial: ->
        selection = {}

        try
            self = @

            checkbox_all_sel = @_tutorial_all_sel.find 'input[type="checkbox"]'

            checkbox_all_sel.change -> self._check_tutorial $(this), checkbox_all_sel
        catch error
            Console.error 'DashboardTutorialActions.event_check_tutorial', error
        finally
            return selection


    _trash_tutorial: ->
        self = @
        string = null

        try
            tutorial_checked_sel = @_tutorial_all_sel.filter ':has(input[name="tutorial_id"]:checked)'
            input_checked_sel = tutorial_checked_sel.find 'input[name="tutorial_id"]'

            page_id = LayoutPage.get_id()

            @_manager_form_sel.ajaxSubmit (data) ->
                if page_id isnt LayoutPage.get_id()
                    return

                if data.status is 'success'
                    tutorial_checked_sel.addClass 'bounceOut animated'
                    tutorial_checked_sel.oneTime(
                        '1s',
                        -> tutorial_checked_sel.remove()
                    )

                self._trash_btn_sel.removeAttr 'disabled'
                self._trash_btn_sel.removeClass 'loading-mask'

                # Notify async system that DOM has been updated
                LayoutPage.fire_dom_updated()

            self._trash_btn_sel.addClass 'loading-mask'
            self._trash_btn_sel.attr 'disabled', true
        catch error
            Console.error 'DashboardTutorialActions._trash_tutorial', error
        finally
            return string


    _confirm_trash_tutorial: (checkbox_checked_size, callback_success_fn) ->
        try
            # Tooltip vars
            tooltip_txt = if checkbox_checked_size is 1 then (@_trash_btn_sel.attr 'data-tooltip-singular') \
                                                        else _.str.sprintf(
                                                                (@_trash_btn_sel.attr 'data-tooltip-plural'),
                                                                checkbox_checked_size
                                                             )
            tooltip_btns = [
                ['Delete', 'danger', (callback_success_fn.bind @)],
                ['Cancel', '']
            ]

            # Create tooltip
            new Tooltip(
                @_trash_btn_sel,
                tooltip_txt,
                tooltip_btns
            )
        catch error
            Console.error 'DashboardTutorialActions._confirm_trash_tutorial', error


    event_trash_tutorial: ->
        try
            self = @

            checkbox_all_sel = @_tutorials_sel.find 'input[type="checkbox"]'

            @_trash_btn_sel.click ->
                checkbox_checked_size = checkbox_all_sel.filter(':checked').size()

                if checkbox_checked_size > 0
                    self._confirm_trash_tutorial(
                        checkbox_checked_size,
                        self._trash_tutorial
                    )
        catch error
            Console.error 'DashboardTutorialActions.event_trash_tutorial', error



@DashboardTutorialActions = new DashboardTutorialActions



$(document).ready ->
    __.DashboardTutorialActions.init()
    __.DashboardTutorialActions.event_search_tutorial()
    __.DashboardTutorialActions.event_check_tutorial()
    __.DashboardTutorialActions.event_trash_tutorial()

    LayoutRegistry.register_bundle 'DashboardTutorialActions'
