###
Bundle: Dashboard Tutorial Root (assets)
Project: Waaave
Authors: Julien Le Coupanec, Valerian Saliou
Copyright: 2014, Hakuma Holdings Ltd.
###

__ = window



class DashboardTutorialRoot
    init: ->
        try
            @_dashboard_sel = $ '.dashboard'
            @_tutorials_sel = $ '.tutorials'
            @_manager_form_sel = @_dashboard_sel.find 'form.manager-form'
            @_tutorial_all_sel = @_tutorials_sel.find '.tutorial'
            @_filter_all_sel = @_manager_form_sel.find '.filter'
            @_filter_val = @_filter_all_sel.filter('.filter-active').attr 'data-val'
        catch error
            Console.error 'DashboardTutorialRoot.init', error


    init_filter_tutorial: ->
        try
            # Attach events
            @_event_filter_tutorial()

            # Start filtering
            @_dashboard_sel.find('.filter-active').click()
        catch error
            Console.error 'DashboardTutorialRoot.init_filter_tutorial', error


    _filter_tutorial: (filter_sel) ->
        try
            @_filter_val = filter_sel.attr 'data-val'
            @update_filter_tutorial filter_sel

            # Trigger search (filters again)
            # Deactivated because was causing filters not to work (due to double hide/show call)
            #if typeof __.DashboardTutorialActions.search_tutorial is 'function'
                #__.DashboardTutorialActions.search_tutorial()
        catch error
            Console.error 'DashboardTutorialRoot._filter_tutorial', error


    update_filter_tutorial: (filter_sel) ->
        try
            if typeof filter_sel is 'undefined'
                if @_filter_val
                    filter_sel = @_filter_all_sel.filter "[data-val='#{@_filter_val}']"
                else
                    filter_sel = @_filter_all_sel.filter ':not([data-val])'

            @_filter_all_sel.removeClass 'filter-active'
            filter_sel.addClass 'filter-active'

            if @_filter_val
                @_tutorial_all_sel.hide()
                @_tutorial_all_sel.filter("[data-filter='#{@_filter_val}']").show()
            else
                @_tutorial_all_sel.show()
        catch error
            Console.error 'DashboardTutorialRoot.update_filter_tutorial', error


    _event_filter_tutorial: (email) ->
        try
            self = @
            @_filter_all_sel.click -> self._filter_tutorial $(this)
        catch error
            Console.error 'DashboardTutorialRoot._event_filter_tutorial', error



@DashboardTutorialRoot = new DashboardTutorialRoot



$(document).ready ->
    __.DashboardTutorialRoot.init()
    __.DashboardTutorialRoot.init_filter_tutorial()

    LayoutRegistry.register_bundle 'DashboardTutorialRoot'
