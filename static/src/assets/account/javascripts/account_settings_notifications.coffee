###
Bundle: Account Settings Notifications (assets)
Project: Waaave
Authors: Julien Le Coupanec, Valerian Saliou
Copyright: 2014, Hakuma Holdings Ltd.
###

__ = window



class AccountSettingsNotifications
    init: ->
        try
            # Selectors
            @_window_sel = $ window
            @_document_sel = $ document
            @_body_sel = @_document_sel.find '.body'
            @_notification_center_sel = @_body_sel.find '.notification-center'
            @_items_sel = @_notification_center_sel.find '.items'
            @_load_more_btn_sel = @_notification_center_sel.find '.show-more'

            # Variables
            @_times_auto_loaded = 0

            # States
            @_is_fetching = false
        catch error
            Console.error 'AccountSettingsNotifications.init', error


    event_fetch_page: ->
        try
            self = @

            @_load_more_btn_sel.find('a.more').click ->
                self._fetch_page()
                return false

            @_window_sel.scroll ->
                if (self._load_more_btn_sel isnt null and self._is_fetching isnt true and self._times_auto_loaded < 2) and
                   (self._window_sel.scrollTop() >= self._body_sel.height() - self._window_sel.height())
                    self._times_auto_loaded++
                    self._fetch_page()
        catch error
            Console.error 'AccountSettingsNotifications.event_fetch_page', error


    _fetch_page: ->
        try
            self = @

            if @_load_more_btn_sel is null
                Console.warn 'AccountSettingsNotifications._fetch_page', 'Nothing more to load...'
                return false

            if @_is_fetching is true
                Console.info 'AccountSettingsNotifications._fetch_page', 'Already fetching data!'
                return false

            @_is_fetching = true

            load_more_url = @_load_more_btn_sel.attr 'data-url'

            if not load_more_url
                Console.warn 'AccountSettingsNotifications._fetch_page', 'Looks like there is nothing to load!'
                return false

            @_load_more_btn_sel.addClass 'loading'

            page_id = LayoutPage.get_id()

            $.get(
                load_more_url,
                (data) ->
                    if page_id isnt LayoutPage.get_id()
                        return

                    data_sel = $ data

                    if (data_sel.is '.notifications')
                        data_items_sel = data_sel.find '.items'
                        data_more_btn_sel = data_sel.find '.show-more'
                        data_page_end_sel = data_sel.find '.page-end'

                        if data_items_sel.size()
                            self._items_sel.append data_items_sel

                            if data_more_btn_sel.size()
                                self._load_more_btn_sel.replaceWith data_more_btn_sel

                                self._load_more_btn_sel = data_more_btn_sel
                                self.event_fetch_page()

                                self._load_more_btn_sel.removeClass 'loading'
                                self._is_fetching = false
                            else
                                self._load_more_btn_sel.replaceWith data_page_end_sel
                                self._load_more_btn_sel = null
                        else
                            self._load_more_btn_sel.replaceWith data_page_end_sel
                    else
                        Console.error 'AccountSettingsNotifications._fetch_page[async]', "#{data.status}:#{data.message}"

                    # Notify async system that DOM has been updated
                    LayoutPage.fire_dom_updated()
            )
        catch error
            Console.error 'AccountSettingsNotifications._fetch_page', error
        finally
            return false



@AccountSettingsNotifications = new AccountSettingsNotifications



$(document).ready ->
    __.AccountSettingsNotifications.init()
    __.AccountSettingsNotifications.event_fetch_page()

    LayoutRegistry.register_bundle 'AccountSettingsNotifications'
