###
Bundle: Account Settings Root (assets)
Project: Waaave
Authors: Julien Le Coupanec, Valerian Saliou
Copyright: 2014, Hakuma Holdings Ltd.
###

__ = window



class AccountSettingsRoot
    init: ->
        try
            # Selectors
            @_window_sel = $ window
            @_document_sel = $ document
            @_body_sel = $ 'body'
            @_avatar_block = $ '.complements .gravatar .avatar'
            @_picture_block = $ '.btn-dropdown-update-picture'
            @_picture_button = $ '.btn-update-picture'
            @_picture_dropdown = @_picture_block.find '.dropdown-toggle'
            @_picture_dropdown_menu = @_picture_block.find '.dropdown-menu'
            @_picture_dropdown_menu_item = $ '.btn-dropdown-update-picture .dropdown-menu li a'

            # Values
            @_picture_api = @_picture_block.attr 'data-api'

            # States
            @_is_update_picture_opened = false
        catch error
            Console.error 'AccountSettingsRoot.init', error


    _open_view: (status_bool, open_fn, close_fn) ->
        try
            if status_bool is false
                if @_has_view_open()
                    @_close_all()

                (open_fn.bind @)()
            else
                (close_fn.bind @)()
        catch error
            Console.error 'AccountSettingsRoot._open_view', error
        finally
            return false


    _has_view_open: ->
        try
            return @_is_update_picture_opened
        catch error
            Console.error 'AccountSettingsRoot._has_view_open', error


    _close_all: ->
        status = false

        try
            if @_is_update_picture_opened is true
                @_close_update_picture()
        catch error
            Console.error 'AccountSettingsRoot._close_all', error
        finally
            return status


    _unbind_all: ->
        try
            @_body_sel.off 'click'
        catch error
            Console.error 'AccountSettingsRoot._unbind_all', error


    event_toggle_update_picture: ->
        try
            self = @

            @_picture_dropdown.on(
                'click',
                -> self._toggle_update_picture()
            )
        catch error
            Console.error 'AccountSettingsRoot.event_toggle_update_picture', error


    _toggle_update_picture: ->
        try
            return @_open_view(
                @_is_update_picture_opened,
                @_open_update_picture,
                @_close_update_picture
            )
        catch error
            Console.error 'AccountSettingsRoot._toggle_update_picture', error


    _open_update_picture: ->
        try
            if not @_picture_dropdown.is '.loading'
                @_picture_dropdown.addClass 'active'
                @_picture_dropdown_menu.fadeIn 100
                @_bind_close_update_picture()

                @_is_update_picture_opened = true
        catch error
            Console.error 'AccountSettingsRoot._open_update_picture', error


    _close_update_picture: ->
        try
            @_picture_dropdown.removeClass 'active'
            @_picture_dropdown_menu.fadeOut 100
            @_unbind_close_update_picture()

            @_is_update_picture_opened = false
        catch error
            Console.error 'AccountSettingsRoot._close_update_picture', error


    _bind_close_update_picture: ->
        try
            self = @

            @_body_sel.on(
                'click',
                (evt) ->
                    try
                        tg = $ evt.target

                        if not (tg.parents('#pictureUpdateDropdown').size() or
                                (tg.is '#pictureUpdateDropdown') or
                                tg.parents('#pictureUpdateDropdownMenu').size() or
                                (tg.is '#pictureUpdateDropdownMenu'))
                            self._close_update_picture()
                    catch _error
                        Console.error 'AccountSettingsRoot._bind_close_update_picture[event:click]', _error
            )
        catch error
            Console.error 'AccountSettingsRoot._bind_close_update_picture', error


    _unbind_close_update_picture: ->
        try
            @_unbind_all()
        catch error
            Console.error 'AccountSettingsRoot._unbind_close_update_picture', error


    event_update_picture_social_networks: ->
        try
            self = @

            @_picture_button.on(
                'click',
                -> self._picture_dropdown_menu_item.filter('.item-active').click()
            )

            @_picture_dropdown_menu_item.on(
                'click',
                ->
                    try
                        if not self._picture_dropdown.is '.loading'
                            self.update_picture_social_network $(this)
                            self._picture_dropdown.addClass 'loading'
                    catch _error
                        Console.error 'AccountSettingsRoot.event_update_picture_social_networks[async]', _error
                    finally
                        return false
            )
        catch error
            Console.error 'AccountSettingsRoot.event_update_picture_social_networks', error


    update_picture_social_network: (element_sel) ->
        try
            self = @

            source_network = element_sel.attr 'data-source'
            csrf_token = @_body_sel.find('input[name="csrfmiddlewaretoken"]:first').val()
            new_social_network = element_sel.html()

            @_picture_dropdown_menu.find('a.item-active').removeClass 'item-active'
            element_sel.addClass 'item-active'

            @_picture_button.html new_social_network
            @_close_update_picture()

            page_id = LayoutPage.get_id()

            if @_picture_api
                $.post(
                    self._picture_api,
                    source: source_network,
                    csrfmiddlewaretoken: csrf_token,
                    (data) ->
                        if page_id isnt LayoutPage.get_id()
                            return

                        if(data.status is 'success')
                            avatar_url = data.contents.url

                            if(avatar_url)
                                self._avatar_block.find('img').attr 'src', avatar_url

                            Console.debug 'AccountSettingsRoot.update_picture_social_network[async]', 'Got success reply'
                        else
                            Console.error 'AccountSettingsRoot.update_picture_social_network[async]', 'Request error (' + (data.message or 'No message') + ')'

                        self._picture_dropdown.removeClass 'loading'

                        # Notify async system that DOM has been updated
                        LayoutPage.fire_dom_updated()
                )
            else
                throw 'No API URL'
        catch error
            Console.error 'AccountSettingsRoot.update_picture_social_network', error



@AccountSettingsRoot = new AccountSettingsRoot



$(document).ready ->
    __.AccountSettingsRoot.init()
    __.AccountSettingsRoot.event_toggle_update_picture()
    __.AccountSettingsRoot.event_update_picture_social_networks()

    LayoutRegistry.register_bundle 'AccountSettingsRoot'
