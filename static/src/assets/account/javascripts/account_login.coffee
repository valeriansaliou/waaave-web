###
Bundle: Account Login (assets)
Project: Waaave
Authors: Julien Le Coupanec, Valerian Saliou
Copyright: 2014, Hakuma Holdings Ltd.
###

__ = window



class AccountLogin
    init: ->
        try
            # Selectors
            @_emblem_bounce_sel = $ '.emblem-img.ef_bounce'
            @_input_email = $ '.credentials .email'
            @_avatar = $ '.avatar-header .picture'

            # Values
            @_host_avatar = $('html').attr 'data-url-avatar'
        catch error
            Console.error 'AccountLogin.init', error


    bounce_info_emblem: ->
        try
            @_emblem_bounce_sel.effect(
                'bounce',
                times: 2,
                350
            )
        catch error
            Console.error 'AccountLogin.bounce_info_emblem', error


    avatar_checking: ->
        try
            self = @

            email = @_input_email.val()
            @_avatar_email_checking email

            @_input_email.keyup ->
                self._avatar_email_checking $(this).val()
        catch error
            Console.error 'AccountLogin.avatar_checking', error


    _avatar_email_checking: (email) ->
        status = false

        try
            if @_validate_email(email)
                @_avatar.attr(
                    'src',
                    @_get_avatar email, 'normal'
                )

                status = true
        catch error
            Console.error 'AccountLogin._avatar_email_checking', error
        finally
            return status


    _validate_email: (email) ->
        try
            re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{1,}))$/

            return re.test email
        catch error
            Console.error 'AccountLogin._validate_email', error


    _get_avatar: (email, size) ->
        try
            url_base = "#{@_host_avatar}#{email}"
            url_size = (if size then ('/' + size + '/') else '')

            return "#{url_base}#{url_size}"
        catch error
            Console.error 'AccountLogin._get_avatar', error



@AccountLogin = new AccountLogin



$(document).ready ->
    __.AccountLogin.init()
    __.AccountLogin.bounce_info_emblem()
    __.AccountLogin.avatar_checking()

    LayoutRegistry.register_bundle 'AccountLogin'
